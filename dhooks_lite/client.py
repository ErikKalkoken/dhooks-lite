import logging
import requests     # noqa


logger = logging.getLogger(__name__)


class WebhookResponse:
    """response from a Discord Webhook"""

    def __init__(
        self, 
        headers: dict, 
        status_code: int, 
        content: dict = None
    ) -> None:
        self._headers = dict(headers)
        self._status_code = int(status_code)
        self._content = dict(content) if content else None

    @property
    def headers(self) -> dict:
        """response headers"""
        return self._headers 

    @property
    def status_code(self) -> int:
        """HTTP status code of the response"""
        return self._status_code 

    @property
    def content(self) -> dict:
        """content of the response, e.g. send report"""
        return self._content 

    @property
    def status_ok(self) -> bool:
        """whether the response was ok based on its HTTP status"""
        return self._status_code >= 200 and self._status_code <= 299


class Webhook:
    MAX_CHARACTERS = 2000

    def __init__(
        self, url: str, username: str = None, avatar_url: str = None
    ) -> None:
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
    ) -> WebhookResponse:
        """Posts a message to this webhook
        
        Parameters
        
        - content: Text of this message
            
        - embeds:List of Embed objects to be attached to this message
            
        - tts: Whether or not the message will use text-to-speech
            
        - username: Overrides default user name of the webhook
        
        - avatar_url: Override default avatar icon of the webhook with image URL
        
        - wait_for_response: Whether or not to wait for a send report 
        from Discord (defaults to ``False``)

        Exceptions
                
        - ValueException: on invalid input

        - ConnectionError: on network issues
        
        - HTTPError: if http code is not 2xx

        - Timeout: if timeouts are exceeded

        - TooManyRedirects: if configured redirect limit is exceeded
        
        Returns
               
        - response from webhook as WebhookResponse object
         
        """                
        if content: 
            content = str(content)
            if len(content) > self.MAX_CHARACTERS:
                raise ValueError(
                    'content exceeds {}'.format(self.MAX_CHARACTERS)
                )
        
        if not content and not embeds:
            raise ValueError('need content or embeds')

        if tts:
            if not isinstance(tts, bool):
                raise TypeError('tts must be of type bool')
                
        payload = dict()
        if content:
            payload['content'] = content
        
        if embeds:            
            payload['embeds'] = self._prepare_embeds(embeds)

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
        logger.debug('Payload to %s: %s', self._url, payload)
        res = requests.post(
            url=self._url, 
            params={'wait': wait_for_response},
            json=payload,
        )

        try:
            content = res.json()
        except ValueError:
            content = None

        response = WebhookResponse(
            headers=res.headers,
            status_code=res.status_code,
            content=content
        )
        
        if logger.getEffectiveLevel() == logging.DEBUG:            
            logger.debug('HTTP status code: %s', response.status_code)
            logger.debug('Response from Discord: %s', response.content)
        else:
            if not response.status_ok:
                logger.warning('HTTP status code: %s', response.status_code)
        
        return response

    def _prepare_embeds(self, embeds: list) -> list:
        if not isinstance(embeds, list):
            raise TypeError('embeds must be of type list')
        
        for embed in embeds:
            if type(embed).__name__ != 'Embed':
                raise TypeError('embeds elements must be of type Embed')
        
        return [x.to_dict() for x in embeds]
