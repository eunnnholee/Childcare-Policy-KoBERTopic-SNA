from selenium import webdriver
import chromedriver_autoinstaller
import time
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 버전 확인
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

def setup_crawler():
    try:
        crawler = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    except:
        chromedriver_autoinstaller.install(True)
        crawler = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    crawler.implicitly_wait(10)
    return crawler

def install_extensions(crawler):
    # 필요한 크롬확장자 설치 (확장자 설치시 확인 버튼 사용자가 눌러야함.)
    url2 = 'https://chrome.google.com/webstore/detail/%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%B9%B4%ED%8E%98-%ED%8C%A8%EC%8A%A4/gipgjcnhbklggnannochejcaieghkmcn?hl=ko'
    crawler.get(url2)
    crawler.find_element('xpath', '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div/div/div/div').click()
    time.sleep(5)
    url3 = 'https://chrome.google.com/webstore/detail/%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%B9%B4%ED%8E%98-%EC%83%88%EB%A1%9C%EA%B3%A0%EC%B9%A8/jlebnhjlcighfebijokkgijldbfiameg?hl=ko'
    crawler.get(url3)
    crawler.find_element('xpath', '/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div/div').click()
    time.sleep(5)

def navercafe(crawler, xpath, n):
    """
    주어진 xpath로 네이버 카페 게시판에 접근하여 크롤링하는 함수.

    Parameters:
    - crawler: webdriver instance
    - xpath: 게시판 링크의 xpath
    - n: 총 페이지 수
    """
    # 게시판 링크 가져오기
    carrier_mom = crawler.find_element('xpath', xpath).get_attribute("href")
    crawler.get(carrier_mom)  # 게시판 링크로 이동
    crawler.switch_to.frame("cafe_main")  # 프레임 전환
    engine = crawler.find_element('xpath', '//*[@id="query"]')
    engine.click()  # 검색 엔진 클릭
    engine.send_keys('육아휴직')  # 검색 키워드 입력
    engine.send_keys(Keys.ENTER)  # 엔터 키 눌러 검색

    title = []
    detail = []

    for i in range(1, n):
        print('----' + str(i) + ' 번째 페이지 -----')
        for a in range(1, 16):  # 각 페이지의 게시물 수
            # 게시물 링크 가져오기
            b = crawler.find_element('xpath', f'//*[@id="main-area"]/div[5]/table/tbody/tr[{a}]/td[1]/div[2]/div/a').get_attribute("href")
            crawler.get(b)  # 게시물 링크로 이동
            crawler.switch_to.frame("cafe_main")  # 프레임 전환
            # 게시물 제목 가져오기
            b = crawler.find_element('xpath', '//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div/h3').text
            print("제목 : " + b)
            title.append(b)
            try:
                # 게시물 내용 가져오기
                b = crawler.find_element('xpath', '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]').text
            except:
                b = crawler.find_element('xpath', '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div/div[1]').text
            print("내용 : " + b, sep='\n')
            detail.append(b)
            time.sleep(1)  # 대기
            crawler.back()  # 이전 페이지로 돌아가기
            time.sleep(1)  # 대기
            crawler.switch_to.frame("cafe_main")  # 프레임 전환

        if i < n - 1:
            if i <= 10:
                if i % 10 != 0:
                    # 다음 페이지로 이동
                    crawler.find_element('xpath', f'//*[@id="main-area"]/div[7]/a[{i % 10} + 1]').click()
                else:
                    crawler.find_element('xpath', '//*[@id="main-area"]/div[7]/a[11]/span').click()
            else:
                if i % 10 != 0:
                    # 다음 페이지로 이동
                    crawler.find_element('xpath', f'//*[@id="main-area"]/div[7]/a[{i % 10} + 2]').click()
                else:
                    crawler.find_element('xpath', '//*[@id="main-area"]/div[7]/a[12]/span').click()
    crawler.get('https://cafe.naver.com/imsanbu')  # 초기 URL로 돌아가기

    return title, detail