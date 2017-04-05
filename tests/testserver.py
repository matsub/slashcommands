#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
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
