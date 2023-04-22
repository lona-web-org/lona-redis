import pickle
import sys

import redis


class RedisSession:
    # FIXME this isn't used - can be removed?
    # def __init__(self, redis_user):
    #   self.redis_user = redis_user

    def __init__(self, *args, **kwargs):
        """
        initalize redis.Redis()

        https://redis.readthedocs.io/en/latest/#quickly-connecting-to-redis

        pass through all kwargs to redis-py
        kwargs:
            https://redis.readthedocs.io/en/latest/connections.html
        """

        self.r = redis.Redis(**kwargs)

    def redis_key(self, user_key):
        """
        combine self.user_request_session_key with user's key
        so that the ACTUAL key used to store value in Redis is unique
        """

        COMBINE_CHR = ":"
        return self.user_request_session_key + COMBINE_CHR + user_key

    def set(self, *args, **kwargs):
        """
        user should call this to easily set values
            eg. request.user.session.set("foo",123)
        pickle all values so that Redis can store any pickle-able Python value

        pass through all kwargs to redis-py .set()
        kwargs:
            https://redis.readthedocs.io/en/latest/commands.html#redis.commands.core.CoreCommands.set
        """

        if len(args) == 2:
            redis_key = self.redis_key(args[0])
            value = pickle.dumps(args[1])

            self.r.set(redis_key, value, **kwargs)

        else:
            class_name = self.__class__.__name__
            function_name = sys._getframe().f_code.co_name
            raise TypeError(
                f"{__name__}.{class_name}.{function_name} expected 2 arguments, got {len(args)}"
            )

    def get(self, *args):
        """
        user should call this to easily get values
            eg. request.user.session.get("foo")
        un-pickle all values that were retrieved from Redis

        if key does not exist, return None
        """

        if len(args) == 1:
            user_key = args[0]
            if self.exists(user_key):
                redis_key = self.redis_key(user_key)
                return pickle.loads(self.r.get(redis_key))
            else:
                return None

        else:
            class_name = self.__class__.__name__
            function_name = sys._getframe().f_code.co_name
            raise TypeError(
                f"{__name__}.{class_name}.{function_name} expected 1 argument, got {len(args)}"
            )

    def exists(self, user_key):
        """
        check if user_key exists
        eg. request.user.session.exists("foo")

        return True/False
        """

        redis_key = self.redis_key(user_key)
        return self.r.exists(redis_key) == 1


# FIXME this isn't used - can be removed?
# class RedisUser:
#    def __init__(self, connection):
#        # self.connection = connection
#        # self.session = RedisSession(self)
#        pass
#
#    def __eq__(self, other):
#        raise NotImplementedError()


class RedisSessionMiddleware:
    async def on_startup(self, data):
        """
        initalize Redis connection

        get settings from app.settings.REDIS_CONNECTION
        """

        settings = data.server.settings

        self.redis_session = RedisSession(**settings.REDIS_CONNECTION)

        # initalize this here, but to be set in handle_request()
        # just prior to user calling request.user.session.get(), request.user.session.set()
        self.user_request_session_key = None

        return data

    # FIXME this isn't used - can be removed?
    # def handle_connection(self, data):
    #    # connection.user = RedisUser(data.connection)
    #
    #    return data

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
