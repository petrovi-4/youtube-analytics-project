import os

from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.channels().list(
            part='snippet,statistics', id=self.channel_id
        )
        response = request.execute()

        if 'items' in response:
            channel_data = response['items'][0]

            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            print(f"Title: {snippet['title']}")
            print(f'Description: {snippet['description']}')
            print(f'View Count: {statistics['viewCount']}')
            print(f'Subscriber Count: {statistics['subscriberCount']}')
        else:
            print('Failed to retrieve data.')
