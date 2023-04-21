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

app.settings.SESSIONS = True
app.settings.MIDDLEWARES = [
    "lona_redis.middlewares.RedisSessionMiddleware",
]

# app.settings.REDIS_USER = "some_redis_user"
# app.settings.REDIS_PASSWORD = "abcd1234"

# FIXME suggested way to pass Redis connection settings
# there are many many kwargs: https://redis.readthedocs.io/en/latest/connections.html
# app.settings.REDIS_CONNECTION = {"password": "abcd1234", "decode_responses": False}
app.settings.REDIS_CONNECTION = {"password": "abcd1234"}
# app.settings.REDIS_CONNECTION = {}


@app.route("/")
class Index(View):
    def handle_request(self, request):
        #
        # NOTE THE "EASY" WAY
        # NOTE examples of using request.user.session.set, request.user.session.get
        #

        # NOTE set single value
        # request.user.session.set(foo=999)
        request.user.session.set("foo", 999)
        # testing throw error
        # request.user.session.set("foo", 999, 345)

        # NOTE get single value
        foo = request.user.session.get("foo")
        logger.debug(f"{foo=}")

        # NOTE set multiple values
        request.user.session.set(foo=123, bar=4.56, baz="hello world")

        # NOTE get multiple values
        var_foo, var_bar, var_baz = request.user.session.get("foo", "bar", "baz")
        logger.debug(f"{var_foo=}, {var_bar=}, {var_baz=}")

        # NOTE store various types of values
        request.user.session.set(str_var="hello world")
        request.user.session.set(list_var=[1, 2.222, "hello world"])
        request.user.session.set(int_var=123)
        request.user.session.set(float_var=123.456)
        request.user.session.set(tuple_var=(1, 2, 3))
        request.user.session.set(dict_var={"a": 1, "b": 2})
        request.user.session.set(boolean_var=True)
        request.user.session.set(
            mixed_var_1=[
                True,
                {"a": 1, "b": 2},
                (1, 2, 3),
                123.456,
                123,
                [1, 2.222, "hello world"],
                "hello world",
            ]
        )
        request.user.session.set(
            mixed_var_2={
                "a": [1, 2, 3],
                "b": {"a": 1, "b": 2},
                "c": (4, 5, 6),
            }
        )

        logger.debug(f"{request.user.session.get('str_var')=}")
        logger.debug(f"{request.user.session.get('list_var')=}")
        logger.debug(f"{request.user.session.get('int_var')=}")
        logger.debug(f"{request.user.session.get('float_var')=}")
        logger.debug(f"{request.user.session.get('tuple_var')=}")
        logger.debug(f"{request.user.session.get('dict_var')=}")
        logger.debug(f"{request.user.session.get('boolean_var')=}")
        logger.debug(f"{request.user.session.get('mixed_var_1')=}")
        logger.debug(f"{request.user.session.get('mixed_var_2')=}")

        #
        # NOTE examples of using Redis commands directly
        # https://redis.readthedocs.io/en/latest/commands.html#core-commands
        #

        # NOTE set key directly in Redis
        # NOTE just an example, DON'T DO THIS
        # should always use request.user.session.redis_key()
        # Otherwise another session will overwrite this key
        request.user.session.r.set("myKey", "thevalueofmykey")
        myKey = request.user.session.r.get("myKey")

        # NOTE Set the value of key name to value if key doesn’t exist
        # request.user.session.r.setnx(request.user.session.redis_key("count"), 1)

        # Increments the value of key by amount. If no key exists, the value will be initialized as amount
        count = request.user.session.r.incr(
            request.user.session.redis_key("count"), amount=1
        )

        # NOTE when using r.get, value returned is in bytes - need to manage this yourself
        count = request.user.session.r.get(request.user.session.redis_key("count"))

        logger.debug(f"{count=}")

        # NOTE show all keys
        all_keys = request.user.session.r.keys()
        logger.debug(f"{all_keys=}")

        # return HTML(H1(request.user.session["count"]))
        return HTML(
            H1("Hello World"),
            # P("Lorem Ipsum"),
        )


app.run()
