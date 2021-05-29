from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time

keyword = '(서울) 2021.05.29 7경주'
url = 'https://www.youtube.com/results?search_query={}'.format(keyword)

driver = webdriver.Chrome('./chromedriver.exe')
driver.get(url)
soup = bs(driver.page_source, 'html.parser')
driver.close()

#name = soup.select('a#video-title')
video_url = soup.select('a#video-title')
#view = soup.select('a#video-title')


url_list = []


'''for i in range(len(name)):
    name_list.append(name[i].text.strip())
    view_list.append(view[i].get('aria-label').split()[-1])'''

url_list.append('{}{}'.format('https://www.youtube.com', video_url[0].get('href')))

'''youtubeDic = {
    '제목': name_list,
    '주소': url_list,
    '조회수': view_list
}'''

#youtubeDf = pd.DataFrame(youtubeDic)

print(url_list[0])

#youtubeDf.to_csv('오마이걸유튜브.csv', encoding='', index=False)

