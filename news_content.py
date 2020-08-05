#!/usr/bin/env python

import sys
import datetime
import simplejson
import requests
import MySQLdb
from bs4 import BeautifulSoup  # pip install beautifulsoup4

from models import News, db
db.create_all()

S_TAG = '<!--repaste.body.begin-->'
E_TAG = '<!--repaste.body.end-->'

def get_soup(url):
    html = requests.get(url).content
    s = html.find(S_TAG)
    if s < 0:
        return None
    e = html.find(E_TAG, s)
    content = html[s:e+len(E_TAG)]
    soup = BeautifulSoup(content)
    return soup


def get_content(href):
    soup = get_soup(href)
    if not soup:
        return ""
    plist = soup.find_all("p")
    s = ""
    for p in plist:
        s += p.text
    return s


def get_daylist(startday, endday):
    daylist = []
    while startday <= endday:
        daylist.append(startday)
        startday = startday + datetime.timedelta(days=1)
    return daylist


def main(someday):
    day = int(someday.strftime("%Y%m%d"))
    objs = News.query.get_by_day(day)
    for o in objs:
        try:
            content = get_content(o.url)
            o.content = content.encode("utf8").decode("utf8")
            db.session.add(o)
        except Exception as e:
            import traceback
            print(traceback.format_exe())
    db.session.commit()




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


