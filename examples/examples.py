import datetime
import os

from dhooks_lite import Webhook, Embed

if 'DISCORD_WEBHOOK_URL' not in os.environ:
    raise ValueError(
        'mandatory environment variable "DISCORD_WEBHOOK_URL" not set'
    )

hook = Webhook(
    os.environ['DISCORD_WEBHOOK_URL'],
    username='Jonny Goodfellow',
    avatar_url='https://imageserver.eveonline.com/Alliance/498125261_128.png'
)
hook.send('Hello world')

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
r = hook.send('abc', embeds=[e])
print(r)

