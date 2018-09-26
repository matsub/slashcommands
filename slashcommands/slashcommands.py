# coding: utf-8

from sanic import Sanic
from sanic.response import json
from .errors import (
    InvalidRequest,
    InvalidToken,
    RouteDuplicated,
    init_handler,
)


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
        error_handler=init_handler()
        app = Sanic(error_handler=init_handler())
        self.app = app
        self.run = self.app.run

        # settings for slash commands
        self.token = token
        self.prefix = prefix.rstrip('/')

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
        self.app.add_route(handler, pattern, methods=frozenset({'POST'}))

    def route(self, path):
        def _route(f):
            async def __route(*args, **kwargs):
                # get request that exactly formal
                request = args[0]
                body = request.form
                print(body)
                if (body is None) or ('token' not in body):
                    raise InvalidRequest

                # verify token
                token = body['token'][0]
                if not self.is_valid(token):
                    raise InvalidToken

                # response
                res = f(body)
                response = format_response(res)
                return json(response)

            # add route
            pattern = self.prefix, path.lstrip('/')
            pattern = '/'.join(pattern)
            self.add_route(pattern, __route)

            return __route
        return _route

    def install(self, app):
        for pattern, handler in app.get_routes():
            self.add_route(pattern, handler)
