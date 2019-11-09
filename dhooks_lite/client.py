import logging
import requests
import datetime
import json


logger = logging.getLogger(__name__)


class Webhook:    
    MAX_CHARACTERS = 2000

    def __init__(self, url: str, username: str = None, avatar_url: str = None):
        self._url = url
        self._username = username
        self._avatar_url = avatar_url        
    
        
    def send(
            self, 
            content: str = None,            
            embeds: list = None,
            tts: bool = None,
            username: str = None, 
            avatar_url: str = None,
            wait_for_response: bool = True
        ):
        # input validation
        if content and len(content) > self.MAX_CHARACTERS:
            raise ValueError('content exceeds {}'.format(self.MAX_CHARACTERS))

        if not content and not embeds:
            raise ValueError('need content or embeds')
        
        # compose payload
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
            payload['username'] = username

        if not avatar_url and self._avatar_url:
            avatar_url = self._avatar_url
        if avatar_url:
            payload['avatar_url'] = avatar_url

        # send request to webhook
        logger.info('Trying to send message to {}'.format(self._url))
        logger.debug('Payload to {}: {}'.format(self._url, payload))
        res = requests.post(
            url=self._url, 
            params={'wait': wait_for_response},
            json=payload,
        )
        res.raise_for_status()
        res_json = res.json()
        logger.debug('Response from Discord: {}', format(res_json))
        return res_json
        

    