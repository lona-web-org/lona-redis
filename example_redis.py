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
        # request.user.session.set(foo=123)
        # OR
        # foo = 123
        # request.user.session.set(foo=foo)
        # foo = request.user.session.get("foo")
        # logger.debug(f"{foo=}")
        # logger.debug(f"{request.user.session._actual_redis_key('foo')=}")

        list_var = [1, 2.222, "string"]
        int_var = 123
        float_var = 123.456
        tuple_var = (1, 2, 3)
        dict_var = {"a": 1, "b": 2}

        # NOTE example of using Redis commands directly
        # https://redis.readthedocs.io/en/latest/commands.html#core-commands
        request.user.session.r.set("myKey", "thevalueofmykey")
        myKey = request.user.session.r.get("myKey")
        all_keys = request.user.session.r.keys()
        logger.debug(f"{all_keys=}")

        # return HTML(H1(request.user.session["count"]))
        return HTML(
            H1("Hello World"),
            #    P("Lorem Ipsum"),
        )


app.run()
