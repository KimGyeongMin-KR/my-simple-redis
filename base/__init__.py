import redis
import json
import dataclasses

@dataclasses.dataclass
class BaseRedis(object):
    db: int
    host: str
    port: int
    _conn: redis.Redis|None = None

    @property
    def connect(self) -> redis.Redis:
        if self._conn is None:
            self._conn = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        return self._conn


@dataclasses.dataclass
class JsonBaseRedis(BaseRedis):
    # TODO change to init
    key: str|None = None

    def reset(self):
        self.connect.delete(self.key)

    def set_all(self, value: dict):
        if not isinstance(value, dict):
            ValueError("Dictionary 이어야 합니다")
        self.connect.set(self.key, json.dumps(value))
    
    def set_detail(self, key: str, value):
        self.connect.hset(self.key, key, json.dumps(value))
    
    def get_all(self):
        return json.loads(self.connect.get(self.key))
    
    def get_detail(self, key: str):
        all_data = self.get_all()
        return all_data.get(key, None)
