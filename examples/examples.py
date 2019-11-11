import datetime
import os

from dhooks_lite import Webhook, Embed, Footer, Image, Video, Provider, Author, Field

if 'DISCORD_WEBHOOK_URL' not in os.environ:
    raise ValueError(
        'mandatory environment variable "DISCORD_WEBHOOK_URL" not set'
    )
"""
# Minimal example: Hello World
hook = Webhook(os.environ['DISCORD_WEBHOOK_URL'])
hook.send('Hello, World!')

# Set username and avatar URL
hook = Webhook(
    os.environ['DISCORD_WEBHOOK_URL'], 
    username='Bruce Wayne',
    avatar_url='https://i.imgur.com/thK8erv.png'
)
hook.send('I am Batman!')

# Simple Embed example
hook = Webhook(os.environ['DISCORD_WEBHOOK_URL'])
e = Embed(description='Can you here me?')
send_report = hook.send('Simple Embed example', embeds=[e])

# Example for embed with all parameters
hook = Webhook(os.environ['DISCORD_WEBHOOK_URL'])
e = Embed(    
    description='Can you here me?',
    title='Nyx Supercarrier',
    url='https://zkillboard.com/ship/23913/',
    color=0x5CDBF0,
    thumbnail=Image(
        'https://imageserver.eveonline.com/Render/23913_128.png'
    ),
    timestamp=datetime.datetime.utcnow(),
    footer=Footer(
        'TOP SECRET', 
        'https://previews.123rf.com/images/arcady31/arcady311103/arcady31110300058/9156413-top-secret-stamp.jpg'
    ),
    author=Author(
        'Erik Kalkoken', 
        'https://imageserver.eveonline.com/Character/93330670_64.jpg'
    ),
    provider=Provider(
        'Erik Kalkokens Killboard', 
        'https://zkillboard.com/character/93330670/'
    ),
    fields=[Field('Top Ship', 'Merlin'), Field('2nd Ship', 'Hawk')]
)

send_report = hook.send('abc', embeds=[e], wait_for_response=True)
print(send_report)

"""

# Example for embed with all parameters
hook = Webhook(os.environ['DISCORD_WEBHOOK_URL'])
e = Embed(    
    description='Does this look ok to you?',
    title='Testing Embed',
    url='https://zkillboard.com/ship/23913/',    
    author=Author(
        'Bruce Wayne',
        'https://zkillboard.com/character/93330670/',
        'https://imageserver.eveonline.com/Character/93330670_64.jpg'
    )    
)

send_report = hook.send(
    'here comes another embed', 
    embeds=[e], 
    wait_for_response=True
)
print(send_report)
