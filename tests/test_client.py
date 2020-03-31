# this test script expects the dhooks_lite module to be installed
# in the current environment, e.g. with pip install -e

import unittest
from unittest.mock import Mock, patch

from dhooks_lite.client import Webhook, WebhookResponse
from dhooks_lite import Embed

from . import set_test_logger

MODULE_PATH = 'dhooks_lite.client'
logger = set_test_logger(MODULE_PATH, __file__)


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
    
    def setUp(self):        
        x = Mock()
        x.headers = {'headers': True}
        x.status_code = 200
        x.json.return_value = {'message': True}
        self.response = x
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_webhook_url(self, mock_requests):                        
        mock_requests.post.return_value = self.response

        hook = Webhook('special-url')        
        self.assertEqual(hook.url, 'special-url')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)        
        self.assertEqual(url, 'special-url')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_webhook_url(self, mock_requests):        
        with self.assertRaises(ValueError):
            Webhook(None)

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_content(self, mock_requests):                
        mock_requests.post.return_value = self.response

        hook = Webhook('xxx')        
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertDictEqual(json, {'content': 'Hi there'})        

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_max_character_limit(self, mock_requests):
        hook = Webhook('xxx')
        large_string = 'x' * 2001        
        with self.assertRaises(ValueError):
            hook.execute(large_string)

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_get_send_report(self, mock_requests):         
        mock_requests.post.return_value = self.response

        hook = Webhook('xxx')        
        response = hook.execute('Hi there', wait_for_response=True)        
        self.assertDictEqual(response.content, {'message': True})

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_content_and_embed(self, mock_requests):
        hook = Webhook('xxx')
        with self.assertRaises(ValueError):
            hook.execute()
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_username(self, mock_requests):                
        mock_requests.post.return_value = self.response
        
        hook = Webhook('xxx', username='Bruce Wayne')
        self.assertEqual(hook.username, 'Bruce Wayne')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertIn('username', json)
        self.assertEqual(json['username'], 'Bruce Wayne')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_avatar_url(self, mock_requests):                
        mock_requests.post.return_value = self.response
        
        hook = Webhook('xxx', avatar_url='abc')
        self.assertEqual(hook.avatar_url, 'abc')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)
        self.assertIn('avatar_url', json)
        self.assertEqual(json['avatar_url'], 'abc')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_send_with_tts(self, mock_requests):                
        mock_requests.post.return_value = self.response

        hook = Webhook('abc')        
        hook.execute('Hi there', tts=True)
        url, json = extract_contents(mock_requests)
        self.assertIn('tts', json)
        self.assertEqual(json['tts'], True)

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detect_wrong_tts_type(self, mock_requests):                
        hook = Webhook('abc')        
        with self.assertRaises(TypeError):
            hook.execute('Hi there', tts=int(5))
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_wrong_embeds_type(self, mock_requests):
        hook = Webhook('xxx')                
        with self.assertRaises(TypeError):
            hook.execute('dummy', embeds=int(5))

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_wrong_embeds_element_type(self, mock_requests):
        hook = Webhook('xxx')
        e = [int(5), float(5)]
        with self.assertRaises(TypeError):
            hook.execute('dummy', embeds=e)


class TestWebhookResponse:

    def test_normal(self):
        response = WebhookResponse(
            headers={'headers': True},
            status_code=200,
            content={'content': True}
        )
        self.assertEqual(response.headers, {'headers': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, {'content': True})

        x = WebhookResponse(
            headers={'headers': True},
            status_code=200,
            content=None
        )
        self.assertIsNone(x.content)

    def test_status_ok(self):
        x = WebhookResponse(
            headers={'headers': True},
            status_code=199
        )
        self.assertIsFalse(x.status_ok)

        x = WebhookResponse(
            headers={'headers': True},
            status_code=200
        )
        self.assertIsTrue(x.status_ok)

        x = WebhookResponse(
            headers={'headers': True},
            status_code=300,
            content=None
        )
        self.assertIsFalse(x.status_ok)


class TestWebhookAndEmbed(unittest.TestCase):
    
    def setUp(self):        
        x = Mock()
        x.headers = {'headers': True}
        x.status_code = 200
        x.json.return_value = {'message': True}
        self.response = x

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_send_with_embed_only(self, mock_requests):
        mock_requests.post.return_value = self.response

        hook = Webhook('xxx')        
        e = Embed(description='Hello, world!')        
        hook.execute(embeds=[e])
        url, json = extract_contents(mock_requests)
        self.assertIn('embeds', json)
        self.assertEqual(len(json['embeds']), 1)
        self.assertDictEqual(
            json['embeds'][0], 
            {'description': 'Hello, world!', 'type': 'rich'}
        )

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_add_multiple_embeds(self, mock_requests):
        mock_requests.post.return_value = self.response

        hook = Webhook('xxx')        
        e1 = Embed(description='Hello, world!')
        e2 = Embed(description='Hello, world! Again!')
        hook.execute('How is it going?', embeds=[e1, e2])
        url, json = extract_contents(mock_requests)
        self.assertIn('embeds', json)
        self.assertEqual(len(json['embeds']), 2)
        self.assertDictEqual(
            json['embeds'][0], 
            {'description': 'Hello, world!', 'type': 'rich'}
        )
        self.assertDictEqual(
            json['embeds'][1], 
            {'description': 'Hello, world! Again!', 'type': 'rich'}
        )
