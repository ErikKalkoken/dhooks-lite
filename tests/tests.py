# this test script expects the dhooks_lite module to be installed
# in the current environment, e.g. with pip install -e

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
        self.assertEqual(hook.url, 'special-url')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)        
        self.assertEqual(url, 'special-url')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_webhook_url(self, mock_requests):        
        with self.assertRaises(ValueError):
            hook = Webhook(None)

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_content(self, mock_requests):                
        hook = Webhook('xxx')        
        response = hook.execute('Hi there')
        self.assertIsNone(response)
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
        mock_post = Mock()
        mock_post.json.return_value = {'send': True}
        mock_requests.post.return_value = mock_post
        hook = Webhook('xxx')        
        send_report = hook.execute('Hi there', wait_for_response=True)
        self.assertDictEqual(send_report, {'send': True})

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_detects_missing_content_and_embed(self, mock_requests):
        hook = Webhook('xxx')
        with self.assertRaises(ValueError):
            hook.execute()
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_username(self, mock_requests):                
        hook = Webhook('xxx', username='Bruce Wayne')
        self.assertEqual(hook.username, 'Bruce Wayne')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertIn('username', json)
        self.assertEqual(json['username'], 'Bruce Wayne')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_set_avatar_url(self, mock_requests):                
        hook = Webhook('xxx', avatar_url='abc')
        self.assertEqual(hook.avatar_url, 'abc')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)
        self.assertIn('avatar_url', json)
        self.assertEqual(json['avatar_url'], 'abc')

    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_send_with_tts(self, mock_requests):                
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


class TestEmbedObjectComparing(unittest.TestCase):
    
    def setUp(self):
        self.x1 = Author('Bruce', 'url-1')
        self.x2 = Author('Bruce', 'url-1')
        self.y1 = Author('Bruce', 'url-2')
        self.y2 = Author('Clark', 'url-1')
        self.z = Author('Clark', 'url-2')
            
    def test_objects_are_equal(self):
        self.assertEqual(self.x1, self.x1)
        self.assertEqual(self.x1, self.x2)

    def test_objects_are_not_equal(self):
        self.assertNotEqual(self.x1, self.y1)
        self.assertNotEqual(self.x1, self.y2)
        self.assertNotEqual(self.x1, self.z)
        self.assertNotEqual(self.x1, Footer('Bruce', 'url-1'))


class TestAuthor(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            x = Author(None)

    def test_create_with_name_only(self):
        x = Author('Bruce Wayne')
        self.assertEqual(x.name, 'Bruce Wayne')
        self.assertDictEqual(
            x._to_dict(),
            {
                'name': 'Bruce Wayne'
            }
        )

    def test_create_with_all_params(self):
        x = Author(
            'Bruce Wayne', 
            url='url-1', 
            icon_url='url-2', 
            proxy_icon_url='url-3'
        )
        self.assertEqual(x.name, 'Bruce Wayne')
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.icon_url, 'url-2')
        self.assertEqual(x.proxy_icon_url, 'url-3')
        self.assertDictEqual(
            x._to_dict(),
            {
                'name': 'Bruce Wayne',
                'url': 'url-1',
                'icon_url': 'url-2',
                'proxy_icon_url': 'url-3'
            }
        )

  
class TestField(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            x = Field(name=None, value=None)

    def test_detects_name_limit(self):
        large_string = 'x' * 257
        with self.assertRaises(ValueError):
            x = Field(large_string, value='Batman')

    def test_detects_value_limit(self):
        large_string = 'x' * 1025
        with self.assertRaises(ValueError):
            x = Field(name='Bruce Wayne', value=large_string)
    
    def test_detect_missing_value(self):
        with self.assertRaises(ValueError):
            x = Field(name='Bruce Wayne', value=None)

    def test_detect_missing_name(self):
        with self.assertRaises(ValueError):
            x = Field(name=None, value='Batman')
    
    def test_create_with_name_and_value_only(self):
        x = Field('fruit', 'orange')        
        self.assertEqual(x.name, 'fruit')
        self.assertEqual(x.value, 'orange')
        self.assertEqual(x.inline, True)
        self.assertDictEqual(
            x._to_dict(),
            {
                'name': 'fruit',
                'value': 'orange',
                'inline': True
            }
        )

    def test_create_with_all_params(self):
        x = Field(name='fruit', value='orange', inline=False)       
        self.assertEqual(x.name, 'fruit')
        self.assertEqual(x.value, 'orange')
        self.assertEqual(x.inline, False)
        self.assertDictEqual(
            x._to_dict(),
            {
                'name': 'fruit',
                'value': 'orange',
                'inline': False
            }
        )

    def test_detect_invalid_inline_type(self):
        with self.assertRaises(TypeError):
            x = Field(name='fruit', value='orange', inline=int(5))


class TestFooter(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            x = Footer(None)

    def test_detects_wrong_type_inline(self):                        
        with self.assertRaises(TypeError):
            x = Footer('Justice League', inline=int(1))

    def test_create_with_name_only(self):
        x = Footer('Justice League')
        self.assertEqual(x.text, 'Justice League')
        self.assertDictEqual(
            x._to_dict(),
            {
                'text': 'Justice League'
            }
        )

    def test_create_with_all_params(self):
        x = Footer('Justice League', icon_url='url-1', proxy_icon_url='url-2')  
        self.assertEqual(x.text, 'Justice League')
        self.assertEqual(x.icon_url, 'url-1')
        self.assertEqual(x.proxy_icon_url, 'url-2')
        self.assertDictEqual(
            x._to_dict(),
            {
                'text': 'Justice League',
                'icon_url': 'url-1',
                'proxy_icon_url': 'url-2'
            }
        )


class TestImage(unittest.TestCase):
    
    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            x = Image(None)
    
    def test_create_with_url_only(self):
        x = Image('my-url')        
        self.assertEqual(x.url, 'my-url')
        self.assertDictEqual(
            x._to_dict(),
            {
                'url': 'my-url'
            }
        )
    
    def test_create_with_all_params(self):
        x = Image(url='url-1', proxy_url='url-2', width=500, height=400)
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.proxy_url, 'url-2')
        self.assertEqual(x.width, 500)
        self.assertEqual(x.height, 400)
        self.assertDictEqual(
            x._to_dict(),
            {
                'url': 'url-1',
                'proxy_url': 'url-2',
                'width': 500,
                'height': 400
            }
        )


    def test_detect_invalid_width(self):
        with self.assertRaises(ValueError):
            x = Image('my-url', width=-5)


    def test_detect_invalid_height(self):
        with self.assertRaises(ValueError):
            x = Image('my-url', height=-5)

  
class TestEmbed(unittest.TestCase):

    def test_create_with_description_only(self):
        x = Embed(
            description='They said the age of heroes would never come again.'
        )
        self.assertEqual(
            x.description, 
            'They said the age of heroes would never come again.'
        )
        self.assertEqual(x.type, 'rich')
        self.assertDictEqual(
            x._to_dict(),
            {
                'type': 'rich',
                'description': 'They said the age of heroes would never come again.'
            }
        )

    def test_create_with_full_params(self):
        now = datetime.datetime.utcnow()
        x = Embed(
            title='Justice League',            
            description='They said the age of heroes would never come again.',
            url='url-1',
            timestamp=now,
            color=0x5CDBF0,
            footer=Footer('TOP SECRET', 'url-2', 'url-11'),
            image=Image('url-3', 'url-4', height=200, width=150),
            thumbnail=Thumbnail('url-5', 'url-6', height=100, width=80),                        
            author=Author('Bruce Wayne', 'url-8', 'url-9'),
            fields=[
                Field('fruit', 'orange', False), 
                Field('vegetable', 'onion', True)
            ]
        )
        self.assertEqual(x.title, 'Justice League')
        self.assertEqual(
            x.description, 
            'They said the age of heroes would never come again.'
        )
        self.assertEqual(x.type, 'rich')
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.timestamp, now.isoformat())
        self.assertEqual(x.color, 0x5CDBF0)
        self.assertEqual(x.footer, Footer('TOP SECRET', 'url-2', 'url-11'))
        self.assertEqual(
            x.image, 
            Image('url-3', 'url-4', height=200, width=150)
        )
        self.assertEqual(
            x.thumbnail, 
            Thumbnail('url-5', 'url-6', height=100, width=80)
        )        
        self.assertEqual(x.author, Author('Bruce Wayne', 'url-8', 'url-9'))
        self.assertEqual(
            x.fields, 
            [
                Field('fruit', 'orange', False), 
                Field('vegetable', 'onion', True)
            ]
        )  
        
        self.maxDiff = None
        self.assertDictEqual(
            x._to_dict(),
            {
                'title': 'Justice League',
                'type': 'rich',
                'description': 'They said the age of heroes would never come again.',
                'url': 'url-1',
                'timestamp': now.isoformat(),
                'color': 0x5CDBF0,              
                'image':{
                    'url': 'url-3',
                    'proxy_url': 'url-4',
                    'height': 200,
                    'width': 150
                },
                'thumbnail':{
                    'url': 'url-5',
                    'proxy_url': 'url-6',
                    'height': 100,
                    'width': 80
                },               
                'footer': {
                    'text': 'TOP SECRET',
                    'icon_url': 'url-2',
                    'proxy_icon_url': 'url-11'
                },
                'author': {
                    'name': 'Bruce Wayne',
                    'url': 'url-8',
                    'icon_url': 'url-9'
                },
                'fields': [
                    {
                        'name': 'fruit',
                        'value': 'orange',
                        'inline': False
                    },
                    {
                        'name': 'vegetable',
                        'value': 'onion',
                        'inline': True
                    }
                ]                
            }
        )

    def test_detects_wrong_type_timestamp(self):                        
        with self.assertRaises(TypeError):
            x = Embed(timestamp=int(1))

    def test_detects_wrong_type_footer(self):                        
        with self.assertRaises(TypeError):
            x = Embed(footer=int(1))

    def test_detects_wrong_type_image(self):                        
        with self.assertRaises(TypeError):
            x = Embed(image=int(1))

    def test_detects_wrong_type_thumbnail(self):                        
        with self.assertRaises(TypeError):
            x = Embed(thumbnail=int(1))

    def test_detects_wrong_type_author(self):
        with self.assertRaises(TypeError):
            x = Embed(author=int(1))

    def test_detects_wrong_type_fields_list(self):                        
        with self.assertRaises(TypeError):
            x = Embed(fields=int(1))

    def test_detects_wrong_type_fields_content(self):                        
        with self.assertRaises(TypeError):
            x = Embed(fields=[int(1), Field('x', 1)])

    def test_detects_max_embed_limit(self):                
        description = 'x' * 2000        
        fields = list()
        for x in range(5):
            fields.append(Field(
                name='name' + str(x),
                value='value' + 'x' * 1000
            ))
        with self.assertRaises(ValueError):
            x = Embed(description=description, fields=fields)

    def test_detects_max_description_limit(self):                
        large_string = 'x' * 2049
        with self.assertRaises(ValueError):
            x = Embed(description=large_string)

    def test_detects_max_title_limit(self):                
        large_string = 'x' * 257
        with self.assertRaises(ValueError):
            x = Embed(title=large_string)

    def test_detects_max_fields_limit(self):                
        fields = list()
        for x in range(26):
            fields.append(
                Field(name='name {}'.format(x), value='value {}'.format(x))
            )
        with self.assertRaises(ValueError):
            x = Embed(fields=fields)

    

class TestWebhookAndEmbed(unittest.TestCase):
    
    @patch('dhooks_lite.client.requests', auto_spec=True)
    def test_can_send_with_embed_only(self, mock_requests):
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
    

if __name__ == '__main__':
    unittest.main()