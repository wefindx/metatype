KEYMAP = {
    '_id': 'url',
    '_time': None,
    '_type': None,
    '_auth': None,
    '_intent': None,
    '_drive': None,
}

class Dict(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        for key in KEYMAP:
            if KEYMAP[key] is not None:
                setattr(self, key, self.get(KEYMAP[key]))
