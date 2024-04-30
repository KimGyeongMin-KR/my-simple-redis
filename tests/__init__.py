import pytest
from core.json import JsonRedis
from redis import Redis

@pytest.fixture(scope="module")
def redis_server():
    # Redis 서버에 연결
    redis_conn = Redis(host='localhost', port=6379, db=0)
    yield redis_conn
    # 테스트 종료 후 Redis 연결 종료
    redis_conn.close()

@pytest.fixture(scope="module")
def json_redis(request, redis_server):
    redis_conn = redis_server
    json_redis_instance = JsonRedis(redis_conn)
    # Fixture 종료시 Redis 연결 종료
    def teardown():
        redis_conn.close()
    request.addfinalizer(teardown)
    return json_redis_instance

def test_set_get(json_redis):
    key = "test_key"
    value = {"name": "John", "age": 30}
    
    # Set value
    json_redis.set(value, key=key)
    
    # Get value
    retrieved_value = json_redis.get_all()
    assert retrieved_value == {key: value}

def test_get_detail(json_redis):
    key = "test_key"
    value = {"name": "John", "age": 30}
    
    # Set value
    json_redis.set(value, key=key)
    
    # Get detail
    retrieved_detail = json_redis.get_detail(key)
    assert retrieved_detail == value
