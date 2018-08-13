# coding: utf-8

from sanic.handlers import ErrorHandler
from sanic.response import json


class InvalidRequest(Exception):
    """This request is not following Slash command format."""
    status = 400


class InvalidToken(Exception):
    """Token doesn't match."""
    status = 400


class RouteDuplicated(Exception):
    pass


def error_handler(request, exception):
    status = exception.status
    text = exception.__doc__
    print(exception.__doc__)
    return json({'detail': text}, status=status)


def init_handler():
    handler = ErrorHandler()
    handler.add(InvalidRequest, error_handler)
    handler.add(InvalidToken, error_handler)
    return handler
