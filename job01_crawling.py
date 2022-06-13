from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException

def crawling_data():
    try:
        elem = driver.find_element_by_css_selector(f'#frm > div > table > tbody > tr:nth-child({i}) > td:nth-child(4) > div > a').click()
        elem = driver.find_element_by_css_selector('#lyricArea > button > span').click()
        url2 = driver.current_url
        resp = requests.get(url2, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        title = soup.select('#downloadfrm > div > div > div.entry > div.info > div.song_name')
        title = str(title)
        title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)[100:-5]
        titles.append(title)

        artist = soup.select('#downloadfrm > div > div > div.entry > div.info > div.artist > a > span:nth-child(1)')
        artist = str(artist)
        artist = re.compile('[^가-힣a-zA-Z ]').sub(' ', artist)[6:-6]
        artists.append(artist)

        genre = soup.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)')
        genre = str(genre)
        genre = re.compile('[^가-힣a-zA-Z ]').sub(' ', genre)[4:-4]
        genres.append(genre)

        lyric = soup.select('#d_video_summary')
        lyric = str(lyric)
        lyric = lyric.replace('<br/>',' ')[82:-7]
        lyrics.append(lyric)

    except NoSuchElementException:
        print('NoSuchElementException')

lyrics = []
titles= []
artists=[]
genres= []
genre= ['Ballade','Dence','rap_Hiphop','R&B_Soul','indie','Rock_metal','Trot','Fork_Blues']
for n in range(101,952,50):

    url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0400#params%5BgnrCode%5D=GN0400&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=NEW&params%5BsteadyYn%5D=N&po=pageObj&startIndex={}".format(n)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    driver.maximize_window()

    for i in range(1,51):
        try:
            crawling_data()
        except StaleElementReferenceException:
            driver.get(url)
            time.sleep(0.5)
            crawling_data()

        df_section_lyrics = pd.DataFrame(titles, columns=['title'])
        df_section_lyrics['artist'] = artists
        df_section_lyrics['genre'] = genres
        df_section_lyrics['lyric'] = lyrics

        df_music = pd.concat([df_section_lyrics],axis='rows', ignore_index=True)
        driver.back()

    df_music.to_csv('./music_20220401_R&B_Soul.csv',encoding='utf-8-sig',header='false',mode='w')
    driver.close()








