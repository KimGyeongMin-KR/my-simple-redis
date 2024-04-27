import redis
import json
import dataclasses


@dataclasses.dataclass
class BaseRedis:
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
class KeyBaseRedis(BaseRedis):
    key: str = ''

    def __post_init__(self, key, *args, **kwargs):
        if not key:
            key = f"{self.__class__.__name__}_default"
        self.key = key
        super().__post_init_(*args, **kwargs)
    
    def reset(self):
        self.connect.delete(self.key)
