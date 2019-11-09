import datetime
import inspect
import os
import sys
import unittest
from unittest.mock import Mock, patch
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir + "/")

from dhooks_lite import *


class TestWebhookMock(unittest.TestCase):

    def get_content(self, mock_requests):
        url = None
        json = None
        for x in mock_requests.post.call_args:
            if type(x) == dict and 'url' in x:
                url = x['url']
            if type(x) == dict and 'json' in x:
                json = x['json']

        return url, json
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_webhook(self, mock_requests):
                
        hook = Webhook('xxx')        
        hook.send('Hi there')
        url, json = self.get_content(mock_requests)
        
        self.assertEqual(url, 'xxx')
        self.assertDictEqual(json, {'content': 'Hi there'})


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_max_embed(self, mock_requests):
        hook = Webhook('xxx')
        large_string = 'x' * 6000
        e = Embed(description=large_string)
        with self.assertRaises(ValueError):
            hook.send('Hi there', embeds=[e])
        

class TestWebhookReal(unittest.TestCase):
    
    def test_webhook(self):    
        if 'DISCORD_WEBHOOK_URL' in os.environ:
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


if __name__ == '__main__':
    unittest.main()