# coding: utf-8

import unittest
from slashcommands import SlashCommands


class TestSlashCommands(unittest.TestCase):

    def setUp(self):
        self.TOKEN = 'test'
        self.app = SlashCommands(self.TOKEN, prefix='/main/')
        self.subapp = SlashCommands(self.TOKEN, prefix='/sub/')

    def test_token_validation(self):
        validated = self.app.is_valid(self.TOKEN)
        self.assertTrue(validated)

    def test_add_route(self):
        @self.app.route('/test')
        def test_route(body):
            return None

        self.assertTrue('/main/test' in self.app.routes)

    def test_install_app(self):
        @self.subapp.route('/test')
        def test_route(body):
            return None

        self.app.install(self.subapp)
        self.assertTrue('/sub/test' in self.app.routes)
