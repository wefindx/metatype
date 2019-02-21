from metatype.defacto import KEYMAP as DEFACTO_KEYMAP
from metatype.mft1 import KEYMAP as MFT1_KEYMAP
from metatype.jsonld import KEYMAP as JSONLD_KEYMAP


class Dict(dict):
    '''
    Accepts: any dictionary, that optionally has keys specifying:

    '-': item origin
    '*': item schema
    '+': item authorship (identity, keys and permissions)
    '^': item itentionality (fact, possibility, desire)

    https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html

    Returns:
    Dict object, that encodes these attributes to python properties.

    '''

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
