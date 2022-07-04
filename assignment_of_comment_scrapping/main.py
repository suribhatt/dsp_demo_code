from scrapping import Scrapping


# Api key is the key you will get from google console after creating credentials and project for the api credentials
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# see here:- https://prnt.sc/1bhvrsz

# Video id is the id of the video for which client want to import and show its statistics(It will be in the url of the youtube video)
video_id = 'dz7Ntp7KQGA'

#Source is the url of the video in youtube
source = 'https://www.youtube.com/watch?v=dz7Ntp7KQGA'


if __name__ == "__main__":
    scr = Scrapping(api_key, video_id, source)
    scr.get_videos()