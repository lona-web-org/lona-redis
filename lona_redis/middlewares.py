import pickle

import redis
from loguru import logger


class RedisSession:
    # FIXME this isn't used - can be removed?
    # def __init__(self, redis_user):
    #   self.redis_user = redis_user

    def __init__(self, *args, **kwargs):
        """
        initalize redis.Redis()

        https://redis.readthedocs.io/en/latest/#quickly-connecting-to-redis
        https://redis.readthedocs.io/en/latest/examples/connection_examples.html

        there are many many kwargs:
        https://redis.readthedocs.io/en/latest/connections.html
        """

        # FIXME pass kwargs straight through to redis.Redis?
        self.r = redis.Redis(**kwargs)

    def _actual_redis_key(self, user_key):
        """
        combine self.user_request_session_key with user's key
        so that the ACTUAL key used to store value in Redis is unique
        """
        COMBINE_CHR = ":"
        return self.user_request_session_key + COMBINE_CHR + user_key

    def set(self, *args, **kwargs):
        """
        user should call this to easily set values
        eg. request.user.session.set(foo=123)

        pickle all values so that Redis can store any pickle-able Python value
        """
        for user_key, value in kwargs.items():
            actual_redis_key = self._actual_redis_key(user_key)
            # logger.debug(f"{user_key=} {actual_redis_key=} {value=}")
            self.r.set(actual_redis_key, pickle.dumps(value))

    # def get(self, *args, **kwargs):
    #    raise NotImplementedError()

    def get(self, *args):
        """
        user should call this to easily get values
        eg. request.user.session.get("foo")

        un-pickle all values that were retrieved from Redis
        """
        user_key = args[0]
        actual_redis_key = self._actual_redis_key(user_key)
        # logger.debug(f"{user_key=} {actual_redis_key=}")

        return pickle.loads(self.r.get(actual_redis_key))


# FIXME this isn't used - can be removed?
class RedisUser:
    def __init__(self, connection):
        # self.connection = connection
        # self.session = RedisSession(self)
        pass

    def __eq__(self, other):
        raise NotImplementedError()


class RedisSessionMiddleware:
    async def on_startup(self, data):
        """
        initalize Redis connection
        """

        settings = data.server.settings

        # FIXME
        # TODO what should the settings be?
        # TODO there are many kwargs (https://redis.readthedocs.io/en/latest/connections.html)
        # TODO maybe settings should be a dict to override the defaults?

        # logger.debug(f"{settings.REDIS_USER=}")
        # logger.debug(f"{settings.REDIS_PASSWORD=}")

        # default args
        # self.redis_session = RedisSession(host="localhost", port=6379, db=0)

        # FIXME pass kwargs (see above)
        self.redis_session = RedisSession()

        # to be set in handle_request()
        # just prior to user calling request.user.session.get(), request.user.session.set()
        self.user_request_session_key = None

        return data

    def handle_connection(self, data):
        # connection.user = RedisUser(data.connection)
        # logger.debug(f"{dir(data.connection)=}")

        return data

    def handle_request(self, data):
        request = data.request

        # set self.user_request_session_key to request.user.session_key
        # so that subsequent calls by the user to
        # self.redis_session.set, self.redis_session.get
        #   ie. in app->View->handle_request() : request.user.session.set(), request.user.session.get()
        # will have request.user.session_key available
        # we NEED this so that each Redis key is unique to request.user.session_key
        self.redis_session.user_request_session_key = request.user.session_key
        request.user.session = self.redis_session

        return data
