import json
import requests
import pandas as pd
import os

class Scrapping:

    def __init__(self, api_key, video_id, source):
        self.video_id = video_id
        self.api_key = api_key
        self.source = source

    def get_videos(self):
        try:
            url = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=replies,snippet&maxResults=50&videoId=%s&key=%s'%(self.video_id,self.api_key)
            data2 = []
            while True:
                response_data = requests.get(url)
                json_data = json.loads(response_data.content)
                if True:
                    nextpagetoken = json_data['nextPageToken']
                    url = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=replies,snippet&pageToken=%s&maxResults=50&videoId=%s&key=%s'%(nextpagetoken,self.video_id,self.api_key)
                    for data in json_data['items']:
                        data2.append(
                            [self.source, 
                            data['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            data['snippet']['topLevelComment']['snippet']['textDisplay'],
                            data['snippet']['topLevelComment']['snippet']['publishedAt'],
                            data['snippet']['topLevelComment']['snippet']['likeCount'],
                            data['snippet']['totalReplyCount'],
                            ]
                     )
        except:
            pass
        finally:
            if os.path.exists("youtube_scrapping.xlsx"):
                os.remove("youtube_scrapping.xlsx")
            fields = ['Source','Name', 'Comment', 'Time', 'Likes','Reply Count']
            df = pd.DataFrame(data2,columns=fields)
            df.to_excel("youtube_scrapping.xlsx",index=False,encoding='utf-8') 
        return True

