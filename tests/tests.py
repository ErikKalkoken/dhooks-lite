import datetime
import unittest
from unittest.mock import Mock, patch

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
        

if __name__ == '__main__':
    unittest.main()