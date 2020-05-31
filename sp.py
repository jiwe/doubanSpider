from bs4 import BeautifulSoup
import requests
import re
import csv
import time


def processDoubanUrl(url):
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'\
            'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept':'text/html,application/xhtml+xml,application/xml;'\
            'q=0.9,image/webp,*/*;q=0.8'}
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text, 'html.parser')

    content = bsObj.find("div", {"id":"content"})
    tables = content.findAll("table")
    rows = []
    for table in tables:
        row = []
        row.append(table.find("a", {"title":re.compile(".*")})["title"])
        author = table.find("p", {"class":"pl"}).get_text()
        row.append(re.match(r'(.*?) /', author).group(1))
        row.append(table.find("span", {"class":"rating_nums"}).get_text())
        row.append(table.find("img")["src"])
        row.append(table.find("a", {"class":"nbg"})["href"])
        rows.append(row)
    return rows


csvFile = open('books.csv', 'wt+')
writer = csv.writer(csvFile)

try:
    for i in range(10):
        url = "https://book.douban.com/top250?start=%d" % (i*25)
        csvRows = processDoubanUrl(url)
        writer.writerows(csvRows)
        time.sleep(1)
finally:
    csvFile.close()

