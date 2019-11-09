import logging
import datetime
import json


logger = logging.getLogger(__name__)


class Embed:
    MAX_CHARACTERS = 6000

    def __init__(
            self, 
            title: str = None, 
            description: str = None, 
            url: str = None, 
            timestamp: datetime = None, 
            color: int = None, 
            image_url: str = None, 
            thumbnail_url: str = None
        ):
        self._title = title
        self._description = description
        self._url = url
        self._timestamp = timestamp
        self._color = color
        self._footer = None
        self._image_url = image_url
        self._thumbnail_url = thumbnail_url
        self._author = None
        self._fields = list()
        self._provider = None
        

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value


    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value   


    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value


    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: str):
        self._timestamp = value    


    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: int):
        self._color = int(value) if value else None
        

    @property
    def image_url(self) -> str:
        return self._image_url

    @image_url.setter
    def image_url(self, value: str):
        self._image_url = value   


    @property
    def thumbnail_url(self) -> str:
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, value: str):
        self._thumbnail_url = value    


    def set_footer(self, name: str, url: str):
        if not name:
            raise ValueError('name can not be None')
        if not url:
            raise ValueError('url can not be None')
        self._footer = {
            'name': name,
            'url': url
        }

    def set_provider(self, text: str, icon_url: str):
        if not text:
            raise ValueError('text can not be None')
        if not icon_url:
            raise ValueError('icon_url can not be None')
        self._footer = {
            'text': text,
            'icon_url': icon_url
        }


    def set_author(self, text: str, url: str, icon_url: str):
        if not text:
            raise ValueError('text can not be None')
        if not url:
            raise ValueError('url can not be None')
        if not icon_url:
            raise ValueError('icon_url can not be None')
        self._footer = {
            'text': text,
            'url': url,
            'icon_url': icon_url
        }


    def add_field(self, name: str, value: str, inline: bool = True):
        if not name:
            raise ValueError('name can not be None')
        if not value:
            raise ValueError('value can not be None')
        self._fields.append({
            'name': name,
            'value': value,
            'inline': inline
        })


    def _to_dict(self):
        d = {
            'type': 'rich'
        }
        if self._title:
            d['title'] = self._title

        if self._description:
            d['description'] = self._description
        
        if self._url:
            d['url'] = self._url

        if self._timestamp:
            d['timestamp'] = self._timestamp.isoformat()

        if self._color:
            d['color'] = self._color

        if self._thumbnail_url:
            d['thumbnail'] = {
                'url': self._thumbnail_url
            }

        if self._image_url:
            d['image'] = {
                'url': self._image_url
            }

        if self._footer:
            d['footer'] = self._footer

        if self._author:
            d['author'] = self._author

        if self._provider:
            d['provider'] = self._provider

        if len(self._fields) > 0:
            d['fields'] = self._fields
        
        d_json = json.dumps(d)
        if len(d_json) > self.MAX_CHARACTERS:
            raise ValueError(
                'Embed exceeds maximum allowed char size of {} by {}'.format(
                    self.MAX_CHARACTERS,
                    len(d_json) - self.MAX_CHARACTERS
                )
            )

        return d
