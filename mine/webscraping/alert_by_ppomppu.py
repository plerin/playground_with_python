import re
import logging
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# 이메일 보내기 위함
import smtplib
from info.account import *
from email.message import EmailMessage


def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Accept-Language": "ko-KR,ko"
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    return BeautifulSoup(res.text, "lxml")


def send_email(list_keyword, content):

    msg = EmailMessage()  # 객체생성
    msg["Subject"] = "alert_by_keyworkd_" + ",".join(list_keyword)  # 제목
    msg["From"] = EMAIL_ADDRESS  # 보내는 사람
    msg["To"] = DESTINATION_ADDRESS  # 받는 사람

    msg.set_content(content)  # 본문

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def scrape_site(max_page, list_keyword):
    dic_content = defaultdict(str)
    total_contents = ''

    for i in range(1, max_page+1):
        url = f"https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page={i}&divpage=69"

        soup = create_soup(url)
        rows = soup.find("table", attrs={"id": "revolution_main_table"}).find_all(
            "tr", attrs={"class": ["list0", "list1"]})

        for row in rows:
            # 종료된 상품이면 패스
            close = row.find(
                "img", attrs={"src": "/zboard/skin/DQ_Revolution_BBS_New1/end_icon.PNG"})
            if close:
                continue

            row_title = row.find(
                "font", attrs={"class": "list_title"}).get_text().replace(" ", "").upper()
            logging.info(row_title)
            try:
                row_link = "https://www.ppomppu.co.kr/zboard/" + row.find(
                    "a", attrs={"href": re.compile("^view.php?")})["href"]
            except TypeError as e:

            for keyword in list_keyword:
                if keyword in row_title:
                    row_link_soup = create_soup(row_link)
                    shop_link = row_link_soup.find(
                        "div", attrs={"class": "wordfix"}).find("a").get_text()
                    dic_content[keyword] += "게시물 이름 : " + row_title + '|'
                    dic_content[keyword] += "게시물 링크 : " + row_link + '|'
                    dic_content[keyword] += "상품 링크 : " + shop_link + '|'

    for keyword in list_keyword:
        total_contents += "="*20 + " " + keyword + " " + "="*20 + "\r\n"

        if dic_content[keyword] == '':
            total_contents += '{}, no search result'.format(keyword) + '\r\n'
        # '\r\n'.join하면 문자열이 개행되면서 합쳐진다.
        total_contents += "\r\n".join(dic_content[keyword].split("|"))
        total_contents += '\r\n'

    return total_contents


if __name__ == "__main__":
    max_page = int(input("검색할 페이지를 입력하세요 : "))
    keywords = input("구매할 물품을 입력하세요(구분자 : ,) :")

    list_keyword = keywords.replace(" ", "").upper().split(",")
    content = scrape_site(max_page, list_keyword)
    send_email(list_keyword, content)
