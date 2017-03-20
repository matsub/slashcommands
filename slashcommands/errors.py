# coding: utf-8


class InvalidRequest(Exception):
    """This request is not following Slash command format."""
    code = 400


class InvalidToken(Exception):
    """Token doesn't match."""
    code = 400


class RouteDuplicated(Exception):
    pass
