# coding: utf-8

from itertools import starmap
from japronto import Application
from .errors import (
    InvalidRequest,
    InvalidToken,
    RouteDuplicated,
)


def error_handler(request, exception):
    code = exception.code
    text = exception.__doc__
    return request.Response(code=code, json={'detail': text})




class SlashCommands:

    def __init__(self, token, prefix='/'):
        # setting japronto up
        app = Application()
        self.app = app
        self.router = app.router
        self.run = self.app.run

        # settings for slash commands
        self.token = token
        self.prefix = prefix.rstrip('/')

        # default Error handlers
        self.app.add_error_handler(InvalidRequest, error_handler)
        self.app.add_error_handler(InvalidToken, error_handler)

    def is_valid(self, token):
        return token == self.token

    def get_routes(self):
        for route in self.router._routes:
            yield route.pattern, route.handler

    def add_route(self, pattern, handler):
        patterns = starmap(lambda p, h: p, self.get_routes())
        if pattern in patterns:
            raise RouteDuplicated(
                "You have already defined `{0}'".format(pattern))
        self.router.add_route(pattern, handler, method='POST')

    def route(self, path):
        def _route(f):
            def __route(*args, **kwargs):
                request = args[0]
                body = request.form
                if (body is None) or ('token' not in body):
                    raise InvalidRequest

                token = body['token']
                if not self.is_valid(token):
                    raise InvalidToken

                response = f(body)
                return request.Response(text=response)

            # add route
            pattern = self.prefix, path.lstrip('/')
            pattern = '/'.join(pattern)
            self.add_route(pattern, __route)

            return __route
        return _route

    def install(self, app):
        for pattern, handler in app.get_routes():
            self.add_route(pattern, handler)
