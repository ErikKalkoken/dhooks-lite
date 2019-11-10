import datetime
import unittest
from unittest.mock import Mock, patch

from dhooks_lite import *


def extract_contents(mock_requests):
    """extract results from mock requests"""
    url = None
    json = None
    for x in mock_requests.post.call_args:
        if type(x) == dict and 'url' in x:
            url = x['url']
        if type(x) == dict and 'json' in x:
            json = x['json']

    return url, json


class TestWebhook(unittest.TestCase):
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_webhook_url(self, mock_requests):                
        hook = Webhook('special-url')        
        hook.send('Hi there')
        url, json = extract_contents(mock_requests)        
        self.assertEqual(url, 'special-url')


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_webhook_url(self, mock_requests):        
        with self.assertRaises(ValueError):
            hook = Webhook(None)


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_content(self, mock_requests):                
        hook = Webhook('xxx')        
        response = hook.send('Hi there')
        self.assertIsNone(response)

        url, json = extract_contents(mock_requests)                
        self.assertDictEqual(json, {'content': 'Hi there'})        


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_max_character_limit(self, mock_requests):
        hook = Webhook('xxx')
        large_string = 'x' * 2001        
        with self.assertRaises(ValueError):
            hook.send(large_string)


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_get_send_report(self, mock_requests):         
        mock_post = Mock()
        mock_post.json.return_value = {'send': True}
        mock_requests.post.return_value = mock_post
        hook = Webhook('xxx')        
        send_report = hook.send('Hi there', wait_for_response=True)
        self.assertDictEqual(send_report, {'send': True})


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_content_and_embed(self, mock_requests):
        hook = Webhook('xxx')
        with self.assertRaises(ValueError):
            hook.send()
    

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_username(self, mock_requests):                
        hook = Webhook('xxx', username='Bruce Wayne')
        hook.send('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertIn('username', json)
        self.assertEqual(json['username'], 'Bruce Wayne')


    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_avatar_url(self, mock_requests):                
        hook = Webhook('xxx', avatar_url='abc')
        hook.send('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertIn('avatar_url', json)
        self.assertEqual(json['avatar_url'], 'abc')
        

class TestEmbed(unittest.TestCase):
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_max_embed_limit(self, mock_requests):
        hook = Webhook('xxx')
        large_string = 'x' * 6001
        e = Embed(description=large_string)
        with self.assertRaises(ValueError):
            hook.send('Hi there', embeds=[e])


if __name__ == '__main__':
    unittest.main()