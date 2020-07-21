#!/usr/bin/env python

import sys
import datetime
import simplejson
import urllib2
import MySQLdb
from bs4 import BeautifulSoup  # pip install beautifulsoup4

URL_FORMAT = "http://tv.cctv.com/lm/xwlb/day/%s.shtml"

from models import News, db
db.create_all()

def get_soup(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

def get_data_by_day(someday):
    url = URL_FORMAT % someday.strftime("%Y%m%d")
    soup = get_soup(url)
    a_list = soup.findAll("a")
    data = []
    num = 0
    day = int(someday.strftime("%Y%m%d"))
    for a in a_list:
        href = a["href"]
        title = a.text.encode("utf8").decode('utf8')
        data.append([day*100 + num, num, day, href, title, datetime.datetime.now()])
        num = num + 1
    return data


def insert_to_db(iterdata):
    for i in iterdata:
        t = News.query.filter(News.id==i[0]).first()
        if not t:
            n = News(
                id=i[0],
                num=i[1],
                day=i[2],
                url=i[3],
                title=i[4],
                created_at=i[5])
            db.session.add(n)
        else:
            t.num = i[1]
            t.day = i[2]
            t.url =i[3]
            t.title = i[4]
            t.updated_at = i[5]
            db.session.add(t)
    db.session.commit()



def get_daylist(startday, endday):
    daylist = []
    while startday <= endday:
        daylist.append(startday)
        startday = startday + datetime.timedelta(days=1)
    return daylist


def main(someday):
    data = get_data_by_day(someday)
    insert_to_db(data)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        someday = datetime.datetime.strptime(sys.argv[1], "%Y%m%d")
        daylist = [someday]
    elif len(sys.argv) == 3:
        startday = datetime.datetime.strptime(sys.argv[1], "%Y%m%d")
        endday = datetime.datetime.strptime(sys.argv[2], "%Y%m%d")
        daylist = get_daylist(startday, endday)
    else:
        someday = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        daylist = [someday]

    for someday in daylist:
        main(someday)

