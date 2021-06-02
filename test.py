from youtubesearchpython import *

videosSearch = VideosSearch('(서울)2021.05.30+10경주', limit=10)

result = videosSearch.result()
for i in range(10):
    print(result['result'][i]['title'], end='->')
    print(result['result'][i]['link'])

