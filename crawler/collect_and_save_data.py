import pandas as pd
from naver_cafe_crawler import setup_crawler, install_extensions, navercafe

def save_to_csv(title, detail):
    # 크롤링 결과 csv파일로 저장
    df = pd.DataFrame({"Title": title, "Detail": detail})
    df["new"] = df["Title"] + " " + df["Detail"]
    df.to_csv("Crawling.csv", encoding="utf-8", index=False)

def main():
    crawler = setup_crawler()
    install_extensions(crawler)
    url = 'https://cafe.naver.com/imsanbu'
    crawler.get(url)

    titles, details = [], []

    # 네이버 카페 게시판 크롤링
    t, d = navercafe(crawler, '//*[@id="menuLink135"]', 101)
    titles.extend(t)
    details.extend(d)

    t, d = navercafe(crawler, '//*[@id="menuLink392"]', 61)
    titles.extend(t)
    details.extend(d)

    t, d = navercafe(crawler, '//*[@id="menuLink126"]', 16)
    titles.extend(t)
    details.extend(d)

    t, d = navercafe(crawler, '//*[@id="menuLink179"]', 101)
    titles.extend(t)
    details.extend(d)

    save_to_csv(titles, details)

if __name__ == "__main__":
    main()