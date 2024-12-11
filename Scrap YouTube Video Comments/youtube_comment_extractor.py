# Functionality: Get YouTube Video link and return all comments in dataframe


from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import pandas as pd
import os

os.environ['YOUTUBE_DATA_API_KEY'] = 'Enter Youtube data API key'

class YouTubeCommentExtractor:
  def __init__(self, url: str):
    self.youtube = build('youtube', 'v3', developerKey= os.environ['YOUTUBE_DATA_API_KEY'])
    self.next_page_token = None
    self.comments = []
    self.url = url
    self.parsed_url = urlparse(self.url)
    if self.parsed_url.netloc in ["youtu.be", "www.youtube.com", "youtube.com"]:
      pass
    else:
      raise ValueError("Invalid YouTube URL")

  def videoId_extract(self):
    if self.parsed_url.netloc == "youtu.be": 
        return self.parsed_url.path[1:]

    if self.parsed_url.path == "/watch":  
        query_params = parse_qs(self.parsed_url.query)
        return query_params.get("v", [None])[0]
    
  def comment_extract(self):
    video_id = self.videoId_extract()
    while True:
      if self.next_page_token is None:
          comments_response = self.youtube.commentThreads().list(
              part='snippet',
              videoId=video_id,
              textFormat='plainText'
          ).execute()
      else:
          comments_response = self.youtube.commentThreads().list(
              part='snippet',
              videoId=video_id,
              pageToken=self.next_page_token,
              textFormat='plainText'
          ).execute()

      self.comments.extend(comments_response['items'])
      self.next_page_token = comments_response.get('nextPageToken')

      if self.next_page_token is None:
          print('Comments Extract successfully, please run comment_clean()')
          break

  def comment_clean(self):
    df = pd.json_normalize(self.comments)
    df = df[['snippet.topLevelComment.snippet.textDisplay',
        'snippet.topLevelComment.snippet.authorDisplayName',
        'snippet.topLevelComment.snippet.publishedAt',
        'snippet.topLevelComment.snippet.likeCount',
              'snippet.totalReplyCount',]]
    df.columns = ['comment', 'author', 'date', 'likes', 'replies']

    return df


# comments = YouTubeCommentExtractor('') # Enter YouTube Video Link 
# comments.comment_extract()
# comments.comment_clean()
