"""
    example_redis.py

    test redis middleware
"""

from lona import App, View
from lona.html import H1, HTML, P

from loguru import logger


# NOTE start Redis before starting this lona script, eg:
# docker run -p 6379:6379 -it redis:latest --requirepass "abcd1234"

app = App(__file__)


# app.settings.SESSIONS = True
app.settings.MIDDLEWARES = [
    "lona_redis.middlewares.RedisSessionMiddleware",
]

# Redis connection settings https://redis.readthedocs.io/en/latest/connections.html
app.settings.REDIS_CONNECTION = {"password": "abcd1234"}
# app.settings.REDIS_CONNECTION = {}


@app.route("/")
class Index(View):
    def handle_request(self, request):
        #
        # NOTE THE "EASY" WAY
        # NOTE examples of using request.user.session.set, request.user.session.get
        #
        session = request.user.session
        session.set("foo", 123)

        # NOTE set
        session.set("foo", 123)
        session.set("foo", 999, ex=5)

        # NOTE exists
        logger.debug(f"{session.exists('foo')=}")
        logger.debug(f"{session.exists('bar')=}")

        # NOTE get
        logger.debug(f"{session.get('foo')=}")
        logger.debug(f"{session.get('bar')=}")

        # NOTE delete
        logger.debug(f"{session.delete('foo')=}")
        logger.debug(f"{session.delete('foo')=}")
        logger.debug(f"{session.delete('bar')=}")

        # NOTE store various types of values
        session.set("str_var", "hello world")
        session.set("list_var", [1, 2.222, "hello world"])
        session.set("int_var", 123)
        session.set("float_var", 123.456)
        session.set("tuple_var", (1, 2, 3))
        session.set("dict_var", {"a": 1, "b": 2})
        session.set("boolean_var", True)
        # session.set(
        #    "mixed_var_1",
        #    [
        #        True,
        #        {"a": 1, "b": 2},
        #        (1, 2, 3),
        #        123.456,
        #        123,
        #        [1, 2.222, "hello world"],
        #        "hello world",
        #    ],
        # )
        # request.user.session.set(
        #    "mixed_var_2",
        #    {
        #        "a": [1, 2, 3],
        #        "b": {"a": 1, "b": 2},
        #        "c": (4, 5, 6),
        #    },
        # )

        # logger.debug(f"{session.get('str_var')=}")
        # logger.debug(f"{session.get('list_var')=}")
        # logger.debug(f"{session.get('int_var')=}")
        # logger.debug(f"{session.get('float_var')=}")
        # logger.debug(f"{session.get('tuple_var')=}")
        # logger.debug(f"{session.get('dict_var')=}")
        # logger.debug(f"{session.get('boolean_var')=}")
        # logger.debug(f"{session.get('mixed_var_1')=}")
        # logger.debug(f"{session.get('mixed_var_2')=}")

        #
        # NOTE examples of using Redis commands directly
        # https://redis.readthedocs.io/en/latest/commands.html#core-commands
        #

        # NOTE set key directly in Redis
        # NOTE just an example, DON'T DO THIS
        # should always use session.redis_key()
        # Otherwise another session will overwrite this key
        # session.r.set("myKey", "thevalueofmykey")
        # myKey = session.r.get("myKey")

        # NOTE Set the value of key name to value if key doesn’t exist
        session.r.setnx(session.redis_key("count"), 1)

        # Increments the value of key by amount. If no key exists, the value will be initialized as amount
        count = session.r.incr(session.redis_key("count"), amount=1)
        logger.debug(f"{count=}")

        # NOTE when using r.get, value returned is in bytes - need to manage this yourself
        count = session.r.get(session.redis_key("count"))
        logger.debug(f"{count=}")

        # NOTE show all keys
        logger.debug(f"{session.r.keys()=}")

        # getset
        # count = session.set("count", 0, get=True)

        return HTML(
            H1("Hello World"),
        )


app.run()
