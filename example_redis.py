"""
    example_redis.py

    test redis middleware
"""

from lona import App, View
from lona.html import H1, HTML, P

from loguru import logger


app = App(__file__)

app.settings.SESSIONS = True
app.settings.MIDDLEWARES = [
    "lona_redis.middlewares.RedisSessionMiddleware",
]

app.settings.REDIS_USER = "some_redis_user"
app.settings.REDIS_PASSWORD = "abcd1234"


@app.route("/")
class Index(View):
    def handle_request(self, request):
        #
        # NOTE examples of using request.user.session.set, request.user.session.get
        #

        # request.user.session.set(foo=123)
        # OR
        # foo = 123
        # request.user.session.set(foo=foo)
        # foo = request.user.session.get("foo")
        # logger.debug(f"{foo=}")
        # logger.debug(f"{request.user.session._actual_redis_key('foo')=}")

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
        #
        # https://redis.readthedocs.io/en/latest/commands.html#core-commands
        request.user.session.r.set("myKey", "thevalueofmykey")
        myKey = request.user.session.r.get("myKey")
        all_keys = request.user.session.r.keys()
        logger.debug(f"{all_keys=}")

        # return HTML(H1(request.user.session["count"]))
        return HTML(
            H1("Hello World"),
            # P("Lorem Ipsum"),
        )


app.run()
