# coding: utf-8

import unittest
import json
import urllib.error
from .webutil import Client
from .testserver import TOKEN


class TestResponse(unittest.TestCase):
    """\
    Basic Testings for SlashCommands

    - Router works correctly
    - Application inheritance
    - 404 Not found
    - 405 Method Not allowed
    - Invalid Request
    - Invalid Token
    """

    def setUp(self):
        self.client = Client('http://localhost:8080/')

    def test_post(self):
        data = {'token': TOKEN}
        expectations = [
            ('/hello/', {"text": "hello!", "response_type": "in_channel"}),
            ('/hello/foo', {"text": "foo!", "response_type": "ephemeral"}),
            ('/sub/', {
                "text": "I'm subapp!",
                "attachments": [{"text": "Partly cloudy today and tomorrow"}]
            }),
        ]

        for url, ans in expectations:
            res = self.client.post(url, data)
            self.assertEqual(res.status, 200)
            res_json = json.loads(res.read().decode())
            self.assertEqual(res_json, ans)

    def test_404(self):
        data = {'token': TOKEN}
        url = '/url/not/exist'

        try:
            res = self.client.post(url, data)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)

    def test_405(self):
        data = {'token': TOKEN}
        url = '/hello/'

        try:
            res = self.client.get(url)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 405)

    def test_InvalidRequest(self):
        data = {'foo': 'bar'}
        url = '/hello/'

        try:
            res = self.client.post(url, data)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
            res_json = json.load(e)
            self.assertTrue('detail' in res_json)
            msg = "This request is not following Slash command format."
            self.assertEqual(res_json['detail'], msg)

    def test_InvalidToken(self):
        data = {'token': 'invalid'+TOKEN}
        url = '/hello/'

        try:
            res = self.client.post(url, data)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
            res_json = json.load(e)
            self.assertTrue('detail' in res_json)
            msg = "Token doesn't match."
            self.assertEqual(res_json['detail'], msg)
