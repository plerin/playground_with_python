import re
import requests
from bs4 import BeautifulSoup

# 이메일 보내기 위함
import smtplib
# from account import *
from email.message import EmailMessage
from selenium import webdriver
# 게시물 url 이용해 게시물 본문확인 위함
# from selenium import webdriver


def create_soup(url):
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        # 만약 페이지가 등록된 header, 국가에 따라 다른 페이지를 제공한다면 한국 페이지 접근하기 위해 필요한 설정
        "Accept-Language": "ko-KR,ko"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def web_test():
    url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page={}&hotlist_flag=999&divpage=64".format(
        1)
    soup = create_soup(url)
    with open("web_test.html", "w", encoding="utf8") as f:
        f.write(soup.prettify())


def send_email(list_keyword, content):

    msg = EmailMessage()  # 객체생성
    msg["Subject"] = "alert_by_keyworkd_" + ",".join(list_keyword)  # 제목
    msg["From"] = EMAIL_ADDRESS  # 보내는 사람
    msg["To"] = "zborisz@naver.com"  # 받는 사람

    msg.set_content(content)  # 본문

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def access_url(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")   # 내부적으로 이 크기로 띄운다.
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()

    url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
    return browser.get(url)


def scrape_ppomppu(max_page, list_keyword):
    dic_content = {}
    total_contents = ''

    for keyword in list_keyword:
        dic_content[keyword] = ''
    for i in range(1, max_page):
        # url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page={}&hotlist_flag=999&divpage=64".format(i)
        url = f"http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page={i}&divpage=67"
        # soup = create_soup(url)

        # res = requests.get(url)
        # res.raise_for_status()  # url에서 데이터를 제대로 받아오지 못한 경우 _ code 400/500 then 에러 발생

        # soup = BeautifulSoup(res.text, "lxml")
        # a = soup.find("table", attrs={"id": "revolution_main_table"})
        # print(a)
        web_test()
        # data_rows = soup.find("table", attrs={"id": "revolution_main_table"}).find_all(
        #     "tr", {"class": ["list0 ", "list1 "]})
    #     for row in data_rows:
    #         close = row.find(
    #             "img", attrs={"src": "/zboard/skin/DQ_Revolution_BBS_New1/end_icon.PNG"})
    #         if close:
    #             continue
    #         row_title = row.find(
    #             "font", attrs={"class": "list_title"}).get_text().replace(" ", "").upper()
    #         row_link = "http://www.ppomppu.co.kr/zboard/" + \
    #             row.find("a", attrs={"href": re.compile("^view.php")})["href"]
    #         print(row_link)
    #         # selenium을 통해 row_link 이동 후 그 안의 진짜 링크를 갖고오자
    #         '''
    #             1. selenium을 통해 페이지 이동하는 방법(click)
    #              - from selenium import webdriver _ webdriver 준비하자
    #              - url를 통해 접근하는 기능 함수로 정의
    #             2. request로 다시 row_link의 html 받아서 사용하는 방법
    #              - 새로운 url를 다시
    #         '''
    #         for keyword in list_keyword:
    #             if keyword in row_title:
    #                 row_link_soup = create_soup(row_link)
    #                 shop_link = row_link_soup.find(
    #                     "div", attrs={"class": "wordfix"}).find("a").get_text()
    #                 dic_content[keyword] += "게시물 이름 : " + row_title + '|'
    #                 dic_content[keyword] += "게시물 링크 : " + row_link + '|'
    #                 dic_content[keyword] += "상품 링크 : " + shop_link + '|'

    # for keyword in list_keyword:
    #     total_contents += "="*20 + " " + keyword + " " + "="*20 + "\r\n"

    #     if dic_content[keyword] == '':
    #         total_contents += '{}, no search result'.format(keyword) + '\r\n'
    #     # '\r\n'.join하면 문자열이 개행되면서 합쳐진다.
    #     total_contents += "\r\n".join(dic_content[keyword].split("|"))
    #     total_contents += '\r\n'
    # print(total_contents)
    # return total_contents


# 프로그램 직접 호출할 때만 사용되도록
if __name__ == "__main__":
    # web_test()

    try:
        print("[alert by keyword | site : ppomppu]")
        max_page = int(input("검색할 최대 페이지를 입력하세요 : "))
        keyword = input("키워드를 입력하세요(구분자 : ,) :")

        list_keyword = keyword.replace(" ", "").upper().split(",")
        content = scrape_ppomppu(max_page, list_keyword)
        # send_email(list_keyword, content)
    except ValueError:
        print("에러! 잘못된 값을 입력했습니다.")
