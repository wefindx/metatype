import os
import yaml

from metatype.defacto import KEYMAP as DEFACTO_KEYMAP
from metatype.mft1 import KEYMAP as MFT1_KEYMAP
from metatype.jsonld import KEYMAP as JSONLD_KEYMAP
from metatype.utils import classproperty, PropertyMeta
from metatype import config

from typology.utils import slug


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
            if keymap.get('id') in self.keys():
                self.id = self.get(keymap.get('id'))
                break

        self.type = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('type') in self.keys():
                self.type = self.get(keymap.get('type'))
                break

        self.auth = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('auth') in self.keys():
                self.auth = self.get(keymap.get('auth'))
                break

        self.intent = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('intent') in self.keys():
                self.intent = self.get(keymap.get('intent'))
                break

        self.drive = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('drive') in self.keys():
                self.drive = self.get(keymap.get('drive'))
                break

    def get_filename(self):
        if hasattr(self, 'id'):
            if self.id is not None:
                s = slug(self.id)
                # POSSIBILITY: to use file extensions to denote short form of type, e.g.:
                #       https-hello-world._Item
                #       https-hello-world.xlsx._Table
                #       https-hello-world.::._Tree
                fname = s[:config.FILENAME_LENGTH_LIMIT-5]+'.yaml'
                return fname

    def get_filedir(self):
        if hasattr(self, 'drive'):
            if self.drive is not None:
                DATA_PATH = os.path.join(config.DATA_DIR, self.drive, type(self).__name__)
            else:
                DATA_PATH = os.path.join(config.DATA_DIR, 'default', type(self).__name__)

            if not os.path.exists(DATA_PATH):
                os.makedirs(DATA_PATH)

            return DATA_PATH

    def save(self):
        path = os.path.join(
            self.get_filedir(),
            self.get_filename()
        )
        with open(path, 'w') as f:
            f.write(yaml.dump(self))
