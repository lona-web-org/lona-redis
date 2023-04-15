class RedisSession:
    def __init__(self, redis_user):
        self.redis_user = redis_user

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def set(self, *args, **kwargs):
        raise NotImplementedError()


class RedisUser:
    def __init__(self, connection):
        self.connection = connection
        self.session = RedisSession(self)

    def __eq__(self, other):
        raise NotImplementedError()


class RedisSessionMiddleware:
    def handle_connection(self, data):
        connection.user = RedisUser(data.connection)

        return data

