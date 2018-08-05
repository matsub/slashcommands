# coding: utf-8

from itertools import starmap
from sanic import Sanic
from .errors import (
    InvalidRequest,
    InvalidToken,
    RouteDuplicated,
)


def error_handler(request, exception):
    code = exception.code
    text = exception.__doc__
    return request.Response(code=code, json={'detail': text})


def not_allowed(request):
    return request.Response(code=405, text='Method Not Allowed')


def format_response(res):
    if isinstance(res, dict):
        return res
    else:
        response = {
            "text": res,
            "response_type": "in_channel",
        }
        return response


class SlashCommands:

    def __init__(self, token, prefix='/'):
        self.routes = dict()

        # setting japronto up
        app = Sanic()
        self.app = app
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
        return self.routes.items()

    def add_route(self, pattern, handler):
        if pattern in self.routes:
            msg = "You have already defined `{0}'".format(pattern)
            raise RouteDuplicated(msg)

        # register the route
        self.routes[pattern] = handler
        self.router.add_route(pattern, handler, method='POST')
        self.router.add_route(pattern, not_allowed, method='GET')

    def route(self, path):
        def _route(f):
            def __route(*args, **kwargs):
                # get request that exactly formal
                request = args[0]
                body = request.form
                if (body is None) or ('token' not in body):
                    raise InvalidRequest

                # verify token
                token = body['token']
                if not self.is_valid(token):
                    raise InvalidToken

                # response
                res = f(body)
                response = format_response(res)
                return request.Response(json=response)

            # add route
            pattern = self.prefix, path.lstrip('/')
            pattern = '/'.join(pattern)
            self.add_route(pattern, __route)

            return __route
        return _route

    def install(self, app):
        for pattern, handler in app.get_routes():
            self.add_route(pattern, handler)
