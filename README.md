# lona-redis

![license MIT](https://img.shields.io/pypi/l/lona-redis.svg)
![Python Version](https://img.shields.io/pypi/pyversions/lona-redis.svg)
![Latest Version](https://img.shields.io/pypi/v/lona-redis.svg)


## Installation

lona-picocss can be installed using pip

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

## What is Redis
Redis is key-value store.

## What is lona-redis
lona-redis uses redis-py to let lona scripts store session data (key-values) in Redis.

lona-redis also allows direct access to the Redis connection for direct execution of Redis commands

## Start up Redis (using Docker)

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

@app.route("/")
class Index(View):
	def handle_request(self, request):
		# set key, value
		request.user.session.set(foo=123)

		# given key, get value
		foo = request.user.session.get("foo")

		return HTML(
            H1("Hello World"),
            # P("Lorem Ipsum"),
        )

```

## More examples of getting & setting session data
```python
```