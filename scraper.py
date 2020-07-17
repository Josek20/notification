from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import requests
import datetime
import re
import newdb

date = datetime.date.today()
day = date.strftime("%d")

anime_titles = {
    # 'Ahiru no Sora':0, 'Black Clover':0,'Monster Musume no Oisha-san':0,'OreGairu':0,'Fire Force Season 2':0,
    # 'Maou Gakuin no Futekigousha: Shijou Saikyou no Maou no Shiso, Tensei shite Shison-tachi no Gakkou e Kayou':0,
    # 'My Teen Romantic Comedy SNAFU Climax':0,'Uzaki-chan wa Asobitai!':0,
    # 'Sword Art Online Alicization War of Underworld (cour 2)':0
}
youtube_channels = {
    # 'Offline tv':'UCDK9qD5DAQML-pzrtA7A4oA',
}

youtube_channels = newdb.receive_ytb(youtube_channels)
anime_titles = newdb.receive_anm(anime_titles)


key = 'AIzaSyBGR52iPLurQG6zIpF5PXaYcJk8vSzrvhY'
service_obj = build('youtube','v3',developerKey=key)

#Create loop with requests for each channel
#using google api
for channel in youtube_channels.keys():
    # print(youtube_channels[channel][1].split('/')[-1])
    request_for_api = service_obj.channels().list(
        part='statistics',
        id=youtube_channels[channel][1].split('/')[-1]#'UCDK9qD5DAQML-pzrtA7A4oA',
    )

    response_from_api = request_for_api.execute()
    new_video_count = response_from_api['items'][0]['statistics']['videoCount']
    if int(youtube_channels[channel][0]) == int(new_video_count):
        print(str(channel)+' '+"No new videos")
        youtube_channels[channel][-1] = 'False\n'
    else:
        print(str(channel)+' '+"There is new video")
        youtube_channels[channel][0] = int(new_video_count)
        youtube_channels[channel][-1] = 'True\n'

#scraper for anime website
page = requests.get("https://darkanime.stream/")
soup = BeautifulSoup(page.content,"html.parser")


last_upload = soup.find_all('h3')
episodes = soup.find_all('span')

for i in last_upload:
    titles_on_page = [k for k in anime_titles.keys() if k in i]
    if len(titles_on_page) != 0:
        new_episode = episodes[last_upload.index(i)]#<span class="series-content-episode-count">E38</span>
        ep = re.search(r"[0-9]*[0-9]",str(new_episode)).group()
        if int(anime_titles[titles_on_page[-1]][0]) != int(ep):
            anime_titles[titles_on_page[-1]][0] = ep
            anime_titles[titles_on_page[-1]][-1] = 'True\n'#new episode just came out
        elif int(day) != newdb.c.execute("SELECT *FROM last_date").fetchall()[-1][0]:
            anime_titles[titles_on_page[-1]][-1] = 'False\n'

 #writing everything back to database
newdb.update_db(anime_titles)
newdb.update_db(youtube_channels)

