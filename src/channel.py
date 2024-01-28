import os
from pprint import pprint
import json

from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self._fetch_channel_data()

    def _fetch_channel_data(self) -> None:
        """Метод для получения данных о канале по API."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
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
        return build('youtube', 'v3', developerKey=API_KEY)

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
    channel = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    pprint(channel.print_info())