'''
purpose : 쿠팡에서 입력된 키워드에 상품 중 할인 중인 물품을 메일 리스트 업

단계
1. input parameter
    - keyword(str) : want to keyword ex) apple, galaxy
    - discount(int) : how to discount now
2. logic
    0) get soup in coupang
    1) search keyword 
    2) get items
    3) find discount items -> filtering
    4) return list by sorted percent of discount

3. add function
    1) sort result set __ sort by discount(%)
    2) add link
    3) 
'''

import requests
from bs4 import BeautifulSoup


def connect_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Accept-Language": "ko-KR,ko"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    return BeautifulSoup(res.text, "lxml")


def scrape_site(keyword, discount):
    for i in range(1, 2):
        # url = f'https://www.coupang.com/np/search?q=%EC%95%A0%ED%94%8C&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={i}&rocketAll=false&searchIndexingToken=&backgroundColor='
        # url = f'https://www.coupang.com/np/search?component=&q={keyword}&channel=user'
        url = f'https://www.coupang.com/np/search?rocketAll=false&q={keyword}&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=60'
        soup = connect_site(url)
        items = soup.find("ul", attrs={"id": "productList"}).find_all(
            "li", attrs={"class": "search-product"})

        for item in items:
            # 로켓 배송 여부
            is_rocket = item.find("span", attrs={"class": "badge rocket"})
            if not is_rocket:
                continue

            # 할인 여부
            is_discount = item.find(
                "span", attrs={"class": "instant-discount-rate"})
            if not is_discount:
                continue
            item_discount = int(is_discount.get_text().split("%")[0])
            if item_discount < discount:
                continue

            # 상품 평 개수 필터링(300개 이상)
            item_rating_cnt = item.find(
                "span", attrs={"class": "rating-total-count"})
            if not item_rating_cnt or int(item_rating_cnt.get_text()[1:-1]) < 300:
                continue

            item_name = item.find("div", attrs={"class": "name"}).get_text()

            print(item_name, item_discount)


if __name__ == "__main__":
    keyword = input("키워드 : ")
    discount = int(input("할인(%)  : "))

    keyword = keyword.replace(" ", "").upper()
    content = scrape_site(keyword, discount)
