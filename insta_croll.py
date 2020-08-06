from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import warnings
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sys

warnings.filterwarnings(action='ignore')

baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

print("Chrome Driver를 실행합니다.")
driver = webdriver.Chrome(
    executable_path="chromedriver.exe"
)
driver.get(url)
time.sleep(3)


# 로그인 하기
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(2)


elem_login = driver.find_element_by_name("username")
elem_login.clear()
#ID 입력하기
elem_login.send_keys('')

elem_login = driver.find_element_by_name('password')
elem_login.clear()
#비밀번호 입력
elem_login.send_keys('')

time.sleep(3)

xpath = """//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button"""
driver.find_element_by_xpath(xpath).click()

time.sleep(30)


# 총 게시물 숫자 불러오기
pageString = driver.page_source
bsObj = BeautifulSoup(pageString, 'lxml')
temp_data = bsObj.find_all(name='meta')[-1]
temp_data = str(temp_data)
start = temp_data.find('게시물') + 4
end = temp_data.find('개')
total_data = temp_data[start:end]
print("총 {0}개의 게시물이 검색되었습니다.".format(total_data))

"""태그 크롤링"""
print("게시물을 수집하는 중입니다.")

SCROLL_PAUSE_TIME = 1.0
reallink = []

while True:
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, 'lxml')
    #v1Nh3 kIKUG _bz0w
    for link1 in bsObj.find_all(name='div', attrs={"class": "Nnq7C weEfm"}):
        for i in range(len(link1.select('a'))):
            title = link1.select('a')[i]
            real = title.attrs['href']
            reallink.append(real)



    last_height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue
    # 게시물의 개수가 계속 바뀌거나 전체 게시물을 가져오지 못한다면
    # 아래 time.sleep의 시간(초)을 늘려주세요.
    time.sleep(3)


# 전체 데이터 및 데이터 배치 사이즈 나누기
num_of_data = len(reallink)
print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))
csvtext = []

for i in tqdm(range(num_of_data)):

    csvtext.append([])
    req = Request("https://www.instagram.com"+reallink[i], headers={'User-Agent': 'Mozila/5.0'})
    try:
        webpage = urlopen(req).read()
    except:
        continue
    soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
    soup1 = soup.find('meta', attrs={'property':"og:description"})

    reallink1 = soup1['content']
    reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
    reallink1 = reallink1[:20]

    if reallink1 == '':
        reallink1 = "Null"
    csvtext[i].append(reallink1)

    for reallink2 in soup.find_all('meta', attrs={'property':"instapp:hashtags"}):
        hashtags = reallink2['content'].rstrip(',')
        csvtext[i].append(hashtags)

    # csv로 저장

    data = pd.DataFrame(csvtext)
    data.to_csv(plusUrl+'insta.txt', encoding='utf-8')

driver.close()