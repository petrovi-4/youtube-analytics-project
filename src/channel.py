import os
from pprint import pprint
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    API_KEY = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self._fetch_channel_data()

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}('{self.__channel_id}', "
                f"'{self.title}', {self.subscriber_count}, {self.video_count}, "
                f"{self.view_count})")

    def __str__(self) -> str:
        return f'{self.title} ({self.url}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count == other.subscriber_count
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count != other.subscriber_count
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count < other.subscriber_count
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count <= other.subscriber_count
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count > other.subscriber_count
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count >= other.subscriber_count
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Channel):
            result = Channel(self.channel_id)
            result.subscriber_count = (
		            (self.subscriber_count or 0) + (other.subscriber_count or 0)
            )
            return result.subscriber_count
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Channel):
            result = Channel(self.channel_id)
            result.subscriber_count -= (
	            (self.subscriber_count or 0) - (other.subscriber_count or 0)
            )
            return result.subscriber_count
        return NotImplemented

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id: str) -> None:
        raise AttributeError(
            f'property "channel_id" of "Channel" object has no setter')

    def _fetch_channel_data(self) -> None:
        """Метод для получения данных о канале по API."""
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        request = youtube.channels().list(
            part='snippet,statistics', id=self.channel_id
        )
        response = request.execute()

        if 'items' in response:
            channel_data = response['items'][0]

            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            self.title = snippet['title']
            self.description = snippet['description']
            self.url = f'https://www.youtube.com/channel/{self.channel_id}'
            self.subscriber_count = int(statistics.get('subscriberCount', 0))
            self.video_count = int(statistics.get('videoCount', 0))
            self.view_count = int(statistics.get('viewCount', 0))

    @classmethod
    def get_service(cls):
        """Класс-метод для получения объекта для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def to_json(self, filename: str) -> None:
        """Метод для сохранения значений атрибутов в JSON-файл."""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f'Channel ID: {self.channel_id}')
        print(f"Title: {self.title}")
        print(f'Description: {self.description}')
        print(f'URL: {self.url}')
        print(f'Subscriber count: {self.subscriber_count}')
        print(f'Video count: {self.video_count}')
        print(f'View Count: {self.view_count}')


if __name__ == '__main__':
    channel1 = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    channel2 = Channel('UC1CchA0SjApw4T-AYkN7ytg')
    pprint(repr(channel1))
    pprint(repr(channel2))
    pprint(str(channel1))
    pprint(str(channel2))
    pprint(channel1 == channel2)
    pprint(channel1 < channel2)
    pprint(channel1 + channel2)
    pprint(channel1 - channel2)
