import datetime
import os

from dhooks_lite import Webhook, Embed

if 'DISCORD_WEBHOOK_URL' not in os.environ:
    raise ValueError(
        'mandatory environment variable "DISCORD_WEBHOOK_URL" not set'
    )

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

# User Embeds
hook = Webhook(os.environ['DISCORD_WEBHOOK_URL'])
e = Embed(
    title='Nyx Supercarrier',
    description='Can you here me?',
    url='https://zkillboard.com/ship/23913/',
    color=0x5CDBF0,
    thumbnail_url='https://imageserver.eveonline.com/Render/23913_128.png',
    timestamp=datetime.datetime.utcnow()
)

e.add_field(name='size', value='large')
e.add_field(name='weight', value='medium')

e.set_footer(
    'Erik Kalkoken', 
    'https://imageserver.eveonline.com/Character/93330670_64.jpg'
)
e.set_provider(
    'Erik Kalkokens Killboard', 
    'https://zkillboard.com/character/93330670/'
)
send_report = hook.send('abc', embeds=[e], wait_for_response=True)
print(send_report)

