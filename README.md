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
