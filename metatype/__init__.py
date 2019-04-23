import os
import yaml

from metatype.defacto import KEYMAP as DEFACTO_KEYMAP
from metatype.mft1 import KEYMAP as MFT1_KEYMAP
from metatype.jsonld import KEYMAP as JSONLD_KEYMAP
from metatype.utils import classproperty, PropertyMeta
from metatype import config

from typology.utils import slug
from metawiki import url2ext

PRIORITY_SEQUENCE = [
    MFT1_KEYMAP,
    JSONLD_KEYMAP,
    DEFACTO_KEYMAP
]

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


    def set_id(self):
        self._id = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('_id') in self.keys():
                self.id = self.get(keymap.get('_id'))
                break

    def set_type(self):
        self._type = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('_type') in self.keys():
                self._type = self.get(keymap.get('_type'))
                break

    def set_auth(self):
        self._auth = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('_auth') in self.keys():
                self._auth = self.get(keymap.get('_auth'))
                break

    def set_intent(self):
        self._intent = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('_intent') in self.keys():
                self._intent = self.get(keymap.get('_intent'))
                break

    def set_drive(self):
        self._drive = None
        for keymap in PRIORITY_SEQUENCE:
            if keymap.get('_drive') in self.keys():
                self._drive = self.get(keymap.get('_drive'))
                break

    def initialize(self):
        self.set_id()
        self.set_type()
        self.set_auth()
        self.set_intent()
        self.set_drive()

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self.initialize()

    def get_filedir(self):
        if not hasattr(self, '_drive'):
            self.set_drive()

        if self._drive is not None:
            DATA_PATH = os.path.join(config.DATA_DIR, self._drive, type(self).__name__)
        else:
            DATA_PATH = os.path.join(config.DATA_DIR, 'default', type(self).__name__)
            print("Since the _drive or profile is not provided, using default directory {}. The object will be non-resumable.".format(DATA_PATH))

        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)

        return DATA_PATH

    def get_extension(self):
        extension = '.yaml'
        sub_extension = '.'

        if hasattr(self, '_type'):
            if isinstance(self._type, str):
                if self._type.startswith('http'):
                    sub_extension += url2ext(self._type)

        extension = sub_extension + extension

    def get_filename(self):
        if not hasattr(self, '_id'):
            self.set_id()

        if self._id is not None:
            slg = slug(self._id)
            ext = self.get_extension()
            fname = slg[config.FILENAME_LENGTH_LIMIT-len(ext):]+ext

        else:
            raise Exception("Can't determine filename without _id. Assign '-' or 'url' key to data, and try again.")

        return fname

    def get_savepath(self):
        dn = self.get_filedir()
        fn = self.get_filename()
        return os.path.join(dn, fn)

    def save(self):
        with open(self.get_savepath(), 'w') as f:
            f.write(yaml.dump(self))
