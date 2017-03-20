# coding: utf-8

import unittest
from slashcommands import SlashCommands
from slashcommands.errors import RouteDuplicated


class TestErrors(unittest.TestCase):

    def setUp(self):
        self.TOKEN = 'test'
        self.app = SlashCommands(self.TOKEN)

    def test_route_duplicate(self):
        with self.assertRaises(RouteDuplicated):
            @self.app.route('/route')
            def route1(body):
                return None

            @self.app.route('/route')
            def route2(body):
                return None
