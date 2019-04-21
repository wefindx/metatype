import os

from metatype.defacto import KEYMAP as DEFACTO_KEYMAP
from metatype.mft1 import KEYMAP as MFT1_KEYMAP
from metatype.jsonld import KEYMAP as JSONLD_KEYMAP
from metatype.utils import classproperty, PropertyMeta

from typology.utils import slug

DATA_DIR = '~/.metadrive/data'
FILENAME_LENGTH_LIMIT = 143 # Cause ecryptfs supports max 143 chars.


class Dict(dict, metaclass=PropertyMeta):
    '''
    Accepts: any dictionary, that optionally has keys specifying:

    '-': item origin
    '*': item schema
    '+': item authorship (identity, keys and permissions)
    '^': item itentionality (fact, possibility, desire)
    '@': (optionally) item metadrive local drive name.

    https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html

    Returns:
    Dict object, that encodes these attributes to python properties.

    '''
    _DRIVES = []

    @classproperty
    def drives(cls):
        return cls._DRIVES

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        PRIORITY_SEQUENCE = [
            MFT1_KEYMAP,
            JSONLD_KEYMAP,
            DEFACTO_KEYMAP
        ]

        self.id = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('id') in self:
                self.id = self.get(keymap.get('id'))
                break

        self.type = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('type') in self:
                self.type = self.get(keymap.get('type'))
                break

        self.auth = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('auth') in self:
                self.auth = self.get(keymap.get('auth'))
                break

        self.intent = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('intent') in self:
                self.intent = self.get(keymap.get('intent'))
                break

        self.drive = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('drive') in self:
                self.drive = self.get(keymap.get('drive'))
                break

    def get_filename(self):
        if hasattr(self, 'id'):
            if self.id is not None:
                s = slug(self.id)
                fname = s[:FILENAME_LENGTH_LIMIT-5]+'.yaml'
                return fname

    def get_filedir(self):
        if hasattr(self, 'drive'):
            if self.drive is not None:
                DATA_PATH = os.path.join(DATA_DIR, self.drive, type(self).__name__)
                return DATA_PATH

    def save(self):
        with open(location, 'w') as f:
            path = os.path.join(
                self.get_filedir(),
                self.get_filename()
            )
            with open(path, 'w') as f:
                f.write(yaml.dump(self))
