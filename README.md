[![wercker status](https://app.wercker.com/status/b529bb3589c645bc2d0cc4c560acb7ee/s/master "wercker status")](https://app.wercker.com/project/byKey/b529bb3589c645bc2d0cc4c560acb7ee)

# slashcommands
A tiny framework for slash commands of Slack.


# Installation

```sh
$ pip install slashcommands
```

And I recommend you the version of Python is over 3.5 at least.


# Usage
Create a program as below,

```python
from slashcommands import SlashCommands

TOKEN = '--- Your Verification Token Here ---'
app = SlashCommands(TOKEN, prefix='/slack/')


@app.route('/')
def hello(body):
    return "hello!"


@app.route('/hey')
def foo(body):
    response = {
        "text": "What'up @{0} !!".format(body['user_name']),
        "response_type": "in_channel",
    }
    return response


if __name__ == '__main__':
    app.run(port=8080)
```

and run it on your server.

The argument `body` is the request from slack.  This is typed as a `dict`
object.  See the [Documentation of Slack](https://api.slack.com/slash-commands#how_do_commands_work)
for the structure of this request.


## Using modules
As your program gets longer, you may want to split it into several files.
To support it, each `SlashCommands` object can inherit another `SlashCommands`
object like,

```python
app = SlashCommands(TOKEN)
subapp = SlashCommands(TOKEN, prefix='/sub/')


@app.route('/')
def hello(body):
    return "hello!"


@subapp.route('/')
def sub(body):
    return "I'm subapp!"


app.install(subapp)
```

now `app` object has additional path `/sub/`.
