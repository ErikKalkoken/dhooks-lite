# dhooks-lite

![license](https://img.shields.io/github/license/ErikKalkoken/dhooks-lite)
![python](https://img.shields.io/pypi/implementation/dhooks-lite)
![version](https://img.shields.io/pypi/v/dhooks-lite)
![build](https://api.travis-ci.org/ErikKalkoken/dhooks-lite.svg?branch=master)
[![codecov](https://codecov.io/gh/ErikKalkoken/dhooks-lite/branch/master/graph/badge.svg)](https://codecov.io/gh/ErikKalkoken/dhooks-lite)
[![Documentation Status](https://readthedocs.org/projects/dhooks-lite/badge/?version=latest)](https://dhooks-lite.readthedocs.io/en/latest/?badge=latest)

## Contents

- [Overview](#Overview)
- [Functionality](#functionality)
- [Examples](#examples)
- [Installation](#installation)
- [Documentation](https://dhooks-lite.readthedocs.io/en/latest/index.html)
- [Change Log](CHANGELOG.md)

## Overview

This is a simple to use class wrapper for posting messages on Discord via webhooks written in Python 3.

dhooks_lite aims to differentiate itself from similar libraries with the following properties:

- runs on any Python 3 version, including older version (e.g. 3.4, 3.5.2)
- is fully tested
- simple interface (only one way of doing things)
- objects and attributes have the same name as in the [official Discord documentation](https://discordapp.com/developers/docs/resources/webhook#execute-webhook)

## Functionality

This library provides a set of classes that implement the following functionality:

- Posting messages in Discord channels via webhooks (synchronous calls only)
- Attaching Embeds to messages (optional)
- Retrieve send reports from Discord (optional)

## Examples

### Hello World

Minimal example for posting a message.

```python
from dhooks-lite import Webhook

hook = Webhook(DISCORD_WEBHOOK_URL)
hook.execute('Hello, World!')
```

![example1](https://i.imgur.com/t3mxMAJ.png)

### Posting with custom avatar

In this example we are setting username and avatar.

```python
from dhooks-lite import Webhook

hook = Webhook(
    DISCORD_WEBHOOK_URL, 
    username='Bruce Wayne',
    avatar_url='https://i.imgur.com/thK8erv.png'
)
hook.execute('I am Batman!')
```

![example2](https://i.imgur.com/mseg2Yx.png)

### Complete example with embeds

Finally, here is an example for posting a message with two embeds and using all available features (shortened):

```python
import datetime
from dhooks_lite import Webhook, Embed, Footer, Image, Thumbnail, Author, Field

hook = Webhook(DISCORD_WEBHOOK_URL)
e1 = Embed(    
    description='Only a few years ago, scientists stumbled upon an electrical current of cosmic proportions.(...)',
    title='Universe\'s highest electric current found',
    url='https://www.newscientist.com/article/mg21028174-900-universes-highest-electric-current-found/',
    timestamp=datetime.datetime.utcnow(),
    color=0x5CDBF0,    
    footer=Footer(
        'Science Department', 
        'https://i.imgur.com/Bgsv04h.png'
    ),    
    image=Image('https://i.imgur.com/eis1Y0P.jpg'),
    thumbnail=Thumbnail('https://i.imgur.com/2A4k28x.jpg'),
    author=Author(
        'John Scientist', 
        url='https://en.wikipedia.org/wiki/Albert_Einstein',
        icon_url='https://i.imgur.com/1JoHDw1.png'
    ),    
    fields=[
        Field('1st Measurement', 'Failed'), 
        Field('2nd Measurement', 'Succeeded')
    ]
)
e2 = Embed(description="TOP SECRET - Do not distribute!")

hook.execute(
    'Checkout this new report from the science department:',
    username='Bruce Wayne',
    avatar_url='https://i.imgur.com/thK8erv.png', 
    embeds=[e1, e2], 
    wait_for_response=True
)
```

![example2](https://i.imgur.com/RoWBh2n.png)

## Installation

You can install this library directly from PyPI:

```bash
pip install dhooks-lite
```
