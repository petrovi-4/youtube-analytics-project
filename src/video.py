import os
from googleapiclient.errors import HttpError
from src.channel import Channel

youtube = Channel.get_service()


class Video:
    API_KEY = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        self.video_id = video_id
        self.title = None
        self.video_url = None
        self.view_count = None
        self.like_count = None

        try:
            self.video_response = youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=self.video_id
            ).execute()
            if self.video_response['items']:
                video_data = self.video_response['items'][0]
                self.title = video_data['snippet']['title']
                self.video_url = f'https://www.youtube.com/{self.video_id}'
                statistics = video_data['statistics']
                self.view_count = int(statistics.get('viewCount', 0))
                self.like_count = int(statistics.get('likeCount', 0))
        except HttpError:
            pass

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
