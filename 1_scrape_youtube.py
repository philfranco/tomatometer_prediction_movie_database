'''
Used to scrape the videos from popular youtube channels that
have movie trailers.
'''

from googleapiclient.discovery import build
import pandas as pd
import json

api_key = 'PUT_HERE'

channel_ids = ['UC2-BeLxzUBSs0uSrmzWhJuQ', # 20th centery
               'UCJ6nMHaJPZvsJ-HmUmj1SeA', # Lions Gate
               'UCWOA1ZGywLbqmigxE4Qlvuw', # Netflix
               'UCjmJDM5pRKbUlVIzDYYWb6g', # Warner Bros
               'UCq0OueAsdxH6b8nyAspwViw', # Universal Pictures
               'UCiifkYAs_bq1pt_zbNAzYGg', # DC
               'UCf5CjDJvsFvtVIhkfmKAwAA', # MGM
               'UCuaFvcY4MhZY3U43mMt1dYQ', # Disney
               'UC_IRYSp4auq7hKLvziWVH6w', # Pixar
               'UCF9imwPMSGz4Vq1NiTWCC7g', # Paramount
               'UCz97F7dMxBNOfGYu3rx8aCw'  # Sony / Columbia
              ]

channel_names = ['20th Century Studios',
                 'Lionsgate Movies',
                 'Netflix',
                 'Warner Bros. Pictures',
                 'Universal Pictures',
                 'DC',
                 'MGM',
                 'Walt Disney Studios',
                 'Pixar',
                 'Paramount Pictures',
                 'Sony Pictures Entertainment'
              ]

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)
channel_data = pd.DataFrame(channel_statistics)

print(channel_data)
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])

def get_video_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()

        for video in response['items']:
          if 'viewCount' in video['statistics'] and 'likeCount' in video['statistics']:
            try:
              video_stats = dict(Title = video['snippet']['title'],
                                 Published_date = video['snippet']['publishedAt'],
                                 Views = video['statistics']['viewCount'],
                                 Likes = video['statistics']['likeCount'],
                                 Favorite = video['statistics']['favoriteCount'],
                                 Comments = video['statistics']['commentCount'],
                                 Description = video ['snippet']['description']
                                 )
            except:
              video_stats = dict(Title = video['snippet']['title'],
                                 Published_date = video['snippet']['publishedAt'],
                                 Views = video['statistics']['viewCount'],
                                 Likes = video['statistics']['likeCount'],
                                 Favorite = video['statistics']['favoriteCount'],
                                 Comments = 0,
                                 Description = video['snippet']['description']
                                 )
            all_video_stats.append(video_stats)

    return all_video_stats

def formatAndSaveJson(channelName, dataPath):
  channels = channel_data.loc[channel_data['Channel_name']==channelName, 'playlist_id'].iloc[0]
  videos = get_video_ids(youtube, channels)
  video_details = get_video_details(youtube, videos)

  with open(dataPath + channelName + '.json', 'w') as f:
    json.dump(video_details, f)

  print('Complete: ' + channelName)


dataPath = "...\\youtube_scrape\\"
for channel in channel_names:
  formatAndSaveJson(channel, dataPath)