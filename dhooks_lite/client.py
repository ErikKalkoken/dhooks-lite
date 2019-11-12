import logging
import requests
import datetime
import json


logger = logging.getLogger(__name__)


class Webhook:    
    MAX_CHARACTERS = 2000

    def __init__(self, url: str, username: str = None, avatar_url: str = None):
        """Initialize a Webhook object
        
        Parameters
        
        - url: Discord webhook url
        - username: Override default user name of the webhook
        - avatar_url: Override default avatar icon of the webhook with image URL

        """
        if not url:
            raise ValueError('url must be specified')

        self._url = url
        self._username = username
        self._avatar_url = avatar_url        
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def username(self) -> str:
        return self._username

    @property
    def avatar_url(self) -> str:
        return self._avatar_url
        
    def execute(
        self, 
        content: str = None,            
        embeds: list = None,
        tts: bool = None,
        username: str = None, 
        avatar_url: str = None,
        wait_for_response: bool = False
    ) -> dict:
        """Posts a message to this webhook
        
        Parameters
        
        - content: Text of this message
            
        - embeds:List of Embed objects to be attached to this message
            
        - tts: Whether or not the message will use text-to-speech
            
        - username: Overrides default user name of the webhook
        
        - avatar_url: Override default avatar icon of the webhook with image URL
        
        - wait_for_response: Whether or not to wait for a send report from Discord (defaults to ``False``)

        Exceptions
                
        - ValueException: on invalid input

        - ConnectionError: on network issues
        
        - HTTPError: if http code is not 2xx

        - Timeout: if timeouts are exceeded

        - TooManyRedirects: if configured redirect limit is exceeded
        
        Returns
               
        - send report when `waiting for response` is `True` else `None`
         

        """        
        if content: 
            content = str(content)
            if len(content) > self.MAX_CHARACTERS:
                raise ValueError(
                    'content exceeds {}'.format(self.MAX_CHARACTERS)
                )

        if embeds:
            if not isinstance(embeds, list):
                raise TypeError('embeds must be of type list')
            for embed in embeds:
                if type(embed).__name__ != 'Embed':
                    raise TypeError('embeds elements must be of type Embed')

        if not content and not embeds:
            raise ValueError('need content or embeds')

        if tts:
            if not isinstance(tts, bool):
                raise TypeError('tts must be of type bool')
                
        payload = dict()
        if content:
            payload['content'] = content
        
        if embeds:            
            payload['embeds'] = [ x._to_dict() for x in embeds ]

        if tts:
            payload['tts'] = tts

        if not username and self._username:
            username = self._username

        if username:
            payload['username'] = str(username)

        if not avatar_url and self._avatar_url:
            avatar_url = self._avatar_url

        if avatar_url:
            payload['avatar_url'] = str(avatar_url)

        # send request to webhook
        logger.info('Trying to send message to {}'.format(self._url))
        logger.debug('Payload to {}: {}'.format(self._url, payload))
        res = requests.post(
            url=self._url, 
            params={'wait': wait_for_response},
            json=payload,
        )
        res.raise_for_status()
        
        if wait_for_response:
            send_report = res.json()
            logger.debug('Response from Discord: {}', format(send_report))
            return send_report
        else:
            return None
        

    