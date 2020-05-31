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
        row.append(table.find("p", {"class":"pl"}).get_text())
        row.append(table.find("span", {"class":"rating_nums"}).get_text())
        #row.append(table.find("img", {"src":re.compile("https:\/\/img3\.doubanio\.com\/view\/subject\/s\/public\/.*\.jpg")})["src"])
        row.append(table.find("img")["src"])
        row.append(table.find("a", {"class":"nbg"})["href"])
        rows.append(row)
    return rows
    # titleList = bsObj.findAll("a", {"title":re.compile(".*")})
    # for title in titleList:
    #     print(title["title"])
        
    # authorList = bsObj.findAll("p", {"class":"pl"})
    # for author in authorList:
    #     print(author.get_text())

    # scoreList = bsObj.findAll("span", {"class":"rating_nums"})
    # for score in scoreList:
    #     print(score.get_text())

    # imageList = bsObj.findAll("img", {"src":re.compile("https:\/\/img3\.doubanio\.com\/view\/subject\/s\/public\/.*\.jpg")})
    # for image in imageList:
    #     print(image["src"])

    # linkList = bsObj.findAll("a", {"class":"nbg"})
    # for link in linkList:
    #     print(link["href"])

    # row = []
    # rows = []
    # for i in range(len(titleList)):
    #     row.append(titleList[i]["title"])
    #     row.append(authorList[i].get_text())
    #     row.append(scoreList[i].get_text())
    #     #row.append(imageList[i]["src"])
    #     #row.append(linkList[i]["href"])
    #     rows.append(row)
    #     row.clear 
    # return rows   

csvFile = open('books.csv', 'wt+')
writer = csv.writer(csvFile)

try:
    count = 0
    for i in range(10):
        url = "https://book.douban.com/top250?start=%d" % (i*25)
        csvRows = processDoubanUrl(url)
        #writer.writerows(csvRows)
        count += len(csvRows)
        time.sleep(1)
    print("All count: %d" % count)
finally:
    csvFile.close()

# for i in range(10):
#     url = "https://book.douban.com/top250?start=%d" % (i*25)
#     processDoubanUrl(url)