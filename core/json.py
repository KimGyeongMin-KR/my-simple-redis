from core.base import KeyBaseRedis


class JsonRedis(KeyBaseRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, value, key=""):
        key = ".".join(["$", key]) if key else "$"
        self.connect.json().set(self.key, key, value)
        return self.get_all()

    def get_all(self):
        doc = self.connect.json().get(self.key, "$")
        if doc is None:
            return {}
        return doc[0]

    def get_detail(self, key):
        value = self.connect.json().get(self.key, key)
        return value
