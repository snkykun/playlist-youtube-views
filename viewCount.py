import schedule
import time
import botkeys
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=botkeys.yt_api_key)

def kyyViewCount():

    kyy_viewCounts = 0
    kyy_nextPageToken = None
    print("working")
    while True:

        # kyy_viewCounts
        kyy_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId='PL5XH1T5EYkawLWSWS4H0WzBE6pn6M1QTY',
                maxResults=50,
                pageToken=kyy_nextPageToken

            )
        kyy_response = kyy_request.execute()
        kyy_nextPageToken = kyy_response.get('nextPageToken')
        for items in kyy_response['items']:
            try:
                kyy_request = youtube.videos().list(
                    part='statistics',
                    id=items['contentDetails']['videoId']
                )
                kyy_response = kyy_request.execute()
                kyy_viewCounts = kyy_viewCounts + int(kyy_response['items'][0]['statistics']['viewCount'])
            except:
                None

        if not kyy_nextPageToken:
            break

    with open('/var/www/html/wp-content/plugins/python-code/views.txt', 'w') as text_file:

        text_file.write(str(kyy_viewCounts))
    requests.post(botkeys.webhook_url, data={"content":"Updated the viewcount of Kyy's editing playlist | ***" + str(format(kyy_viewCounts, ",d")) + "*** views."})


schedule.every(6).hours.do(kyyViewCount)

while True:
	schedule.run_pending()
	time.sleep(1)
