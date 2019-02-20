class Dict(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self.url = self.get('-') or self.get('url')
        self.schema = get_schema(self['*'])
        self.auth = self.get('+')

