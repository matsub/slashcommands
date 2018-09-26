#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import (
    abspath,
    dirname,
)
import sys

this_path = abspath(__file__)
module_path = dirname(dirname(this_path))
sys.path.append(module_path)


from slashcommands import SlashCommands

TOKEN = 'test'
app = SlashCommands(TOKEN, prefix='/hello/')
subapp = SlashCommands(TOKEN, prefix='/sub/')


@app.route('/')
def hello(body):
    return "hello!"


@app.route('/foo')
def hello2(body):
    response = {
        "text": "foo!",
        "response_type": "ephemeral",
    }
    return response


@subapp.route('/')
def foo(body):
    response = {
        "text": "I'm subapp!",
        "attachments": [{"text": "Partly cloudy today and tomorrow"}]
    }
    return response


app.install(subapp)

if __name__ == '__main__':
    app.run(port=8080)
