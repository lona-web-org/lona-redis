# lona-redis

![license MIT](https://img.shields.io/pypi/l/lona-redis.svg)
![Python Version](https://img.shields.io/pypi/pyversions/lona-redis.svg)
![Latest Version](https://img.shields.io/pypi/v/lona-redis.svg)

lona-redis uses Redis as a key-value store to store server side cookies.

lona-redis also allows direct access to the Redis connection for direct execution of Redis commands.

## Installation

lona-redis can be installed using pip

```
pip install lona-redis
```

## Using Sessions

```python
settings.py

MIDDLEWARES = [
    'lona_redis.middlewares.RedisSessionMiddleware',
]
```

## Start up Redis
Using Docker
```
docker run -p 6379:6379 -it redis:latest --requirepass "abcd1234"

# without password
docker run -p 6379:6379 -it redis:latest
```
or (https://developer.redis.com/create/docker/redis-on-docker/)
```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

## Example lona script
```python
from lona import App, View
from lona.html import H1, HTML

app = App(__file__)

app.settings.SESSIONS = True
app.settings.MIDDLEWARES = [
    "lona_redis.middlewares.RedisSessionMiddleware",
]
app.settings.REDIS_CONNECTION = {"password": "abcd1234"}

@app.route("/")
class Index(View):
    def handle_request(self, request):
        session = request.user.session

        # set key, value
        session.set("foo", 123)

        # returns True
        session.exists("foo")

        # given key, get value
        foo = session.get("foo")

        return HTML(
            H1("Hello World"),
        )
```

## Store other data types
Any data type that can be pickled can be stored
```python
session.set("str_var", "hello world")
session.set("list_var", [1, 2.222, "hello world"])
session.set("int_var", 123)
session.set("float_var", 123.456)
session.set("tuple_var", (1, 2, 3))
session.set("dict_var", {"a": 1, "b": 2})
session.set("boolean_var", True)
session.set(
    "mixed_types_var",
    {
        "a": [1, 2, 3],
        "b": {"a": 1, "b": 2},
        "c": (4, 5, 6),
    },
)
```
## Store key-values that expire
Arguments are passed through to Redis set() command

All parameters are available in lona-redis

(https://redis.readthedocs.io/en/latest/commands.html#redis.commands.core.CoreCommands.set)
```python
# "foo" will expire in 5 seconds
session.set("foo", 123, ex=5)
```
### Using Redis commands directly
**Always access the key with session.redis_key()**

```python
# Set the value of key name to value if key doesn’t exist
# https://redis.readthedocs.io/en/latest/commands.html#redis.commands.core.CoreCommands.setnx
session.r.setnx(session.redis_key("count"), 1)

# Increments the value of key by amount. If no key exists, the value will be initialized as amount
# https://redis.readthedocs.io/en/latest/commands.html#redis.commands.core.CoreCommands.incr
count = session.r.incr(session.redis_key("count"), amount=1)

# when using r.get, value returned is in bytes - need to manage this yourself
session.r.get(session.redis_key("count"))
```