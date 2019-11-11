# dhooks-lite

![license](https://img.shields.io/github/license/ErikKalkoken/dhooks-lite)
![python](https://img.shields.io/badge/python-3.4|3.5-informational)
![version](https://img.shields.io/badge/version-0.1.0-orange)
![build](https://api.travis-ci.org/ErikKalkoken/dhooks-lite.svg?branch=master)
[![codecov](https://codecov.io/gh/ErikKalkoken/dhooks-lite/branch/master/graph/badge.svg)](https://codecov.io/gh/ErikKalkoken/dhooks-lite)

## Contents

- [Overview](#Overview)
- [Functionality](#functionality)
- [Examples](#examples)
- [Installation](#installation)

## Overview

This is a simple to use class wrapper for posting messages on Discord via webhooks written in Python 3.

dhooks_lite aims to differentiate itself from similar libraries with the following properties:

- runs on older Python version (e.g. 3.4, 3.5.2)
- is fully tested

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
hook.send('Hello, World!')
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
hook.send('I am Batman!')
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

hook.send(
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
