from googleapiclient.discovery import build
import sqlite3
import os


DataBase_File = 'DataBase.db'
class DatabaseConnection:
    def __init__(self,host):
        self.connection =None
        self.host = host
    def __enter__(self):
        self.connection = sqlite3.connect(self.host,detect_types=sqlite3.PARSE_DECLTYPES)
        return self.connection
    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


def Create_Database():
    with DatabaseConnection(DataBase_File) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS show_skipped(
                    title text NOT NULL,
                    description text NOT NULL,
                    thumbnail_link text NOT NULL UNIQUE,
                    video_link text NOT NULL UNIQUE,
                    channel_name text NOT NULL,
                    publish_time text NOT NULL,
                    searched text NOT NULL,
                    searched_by text NOT NULL
            );""")
        connection.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS show_captured(
                    title text NOT NULL,
                    description text NOT NULL ,
                    thumbnail_link text NOT NULL UNIQUE,
                    video_link text NOT NULL UNIQUE,
                    channel_name text NOT NULL,
                    publish_time text NOT NULL,
                    searched text NOT NULL,
                    searched_by text NOT NULL
            );""")
            
        connection.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS rerun(
                    title text NOT NULL,
                    description text NOT NULL ,
                    thumbnail_link text NOT NULL UNIQUE,
                    video_link text NOT NULL UNIQUE,
                    channel_name text NOT NULL,
                    publish_time text NOT NULL,
                    searched text NOT NULL,
                    searched_by text NOT NULL
            );""")
            
        connection.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS log(
                        id integer primary key not null, 
                        [last_run] timestamp not null,  
                        searched_phrase text not null,
                        schedule text not null,
                        next_run date not null,
                        max_result INTEGER not null,
                        searched_by text not null);""")
        connection.commit()
def Extract_Detail_by_channel(keyword,maxR,order,videoDur):
    with open("Mains/set_api_key.txt","r") as file:
        api_key = file.read().strip()
    youtube = build('youtube','v3',developerKey=api_key)
    req = youtube.search().list(
        q= keyword,
        part = 'snippet',
        type = 'channel',
        maxResults = maxR,
        order = order,
        videoDuration = videoDur
    )
    details = req.execute()
    fetched_channels = []
    for item in details['items']:
        channel_id = item['id']['channelId']
        channel_title = item['snippet']['title']
        channel_description = item['snippet']['description']
        channel_publish = item['snippet']['publishedAt']
        channel_thumbnails =  item['snippet']['thumbnails']['high']
        fetched_channels.append([channel_id,channel_title,channel_description,channel_publish,channel_thumbnails])
    return fetched_channels

def Extract_Detail_of_URL_video(video_id):
    with open("Mains/set_api_key.txt","r") as file:
        api_key = file.read().strip()
    youtube = build('youtube','v3',developerKey=api_key)
    req = youtube.videos().list(
        id = video_id,
        part = 'snippet'
    ).execute()
    videos = []
    for item in req['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnail_link = item['snippet']['thumbnails']['high']['url']
        video_link = item['id']
        channel_name = item['snippet']['channelTitle']
        publish_time = item['snippet']['publishedAt'][:10] + " " + item['snippet']['publishedAt'][-9:-1]
        videos.append([title,description,thumbnail_link,video_link,channel_name,publish_time])
    return videos


def Extract_Details_of_Channel_videos(channel_id):
    with open("Mains/set_api_key.txt","r") as file:
        api_key = file.read().strip()
    youtube = build('youtube','v3',developerKey=api_key)
    req = youtube.channels().list(
        id = channel_id,
        part = 'contentDetails'
    )
    details = req.execute()
    playlist_id = details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos =[]
    next_page_token = None
    while(1):
        res = youtube.playlistItems().list(
        playlistId = playlist_id ,
        part = 'snippet',
        maxResults = 50,
        pageToken = next_page_token)
        res = res.execute()
        for item in res['items']:
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_link = item['snippet']['thumbnails']['high']['url']
            video_link = item['snippet']['resourceId']['videoId']
            channel_name = item['snippet']['channelTitle']
            publish_time = item['snippet']['publishedAt'][:10] + " " + item['snippet']['publishedAt'][-9:-1]
            videos.append([title,description,thumbnail_link,video_link,channel_name,publish_time])
        next_page_token = res.get('nextPageToken')
        if next_page_token is None:
            break
    return videos


def Extract_Detail_by_keyword(keyword ,maxR,order,videoDur):
    with open("Mains/set_api_key.txt","r") as file:
        api_key = file.read().strip()
    youtube = build('youtube','v3',developerKey=api_key)
    fetched_videos = []
    next_page_token = None
    while(1):    
        req = youtube.search().list(
            q= keyword,
            part = 'snippet',
            type = 'video',
            maxResults = 50,
            order = order,
            videoDuration = videoDur,
            pageToken = next_page_token
        )
        detail = req.execute()
        for item in detail['items']:
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_link = item['snippet']['thumbnails']['high']['url']
            video_link = item['id']['videoId']
            channel_name = item['snippet']['channelTitle']
            publish_time = item['snippet']['publishTime'][:10] + " " + item['snippet']['publishTime'][-9:-1]
            fetched_videos.append([title,description,thumbnail_link,video_link,channel_name,publish_time])
            if maxR ==  len(fetched_videos):
                break
        if maxR == len(fetched_videos):
            break
        next_page_token = detail.get('nextPageToken')
    return fetched_videos      

