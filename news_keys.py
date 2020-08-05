#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import simplejson
import MySQLdb

import jieba
import jieba.analyse

from models import News, db
db.create_all()

def get_keyword(content, top_k=10):
    tags = jieba.analyse.extract_tags(content, topK=top_k)
    return " ".join(tags)

def get_daylist(startday, endday):
    daylist = []
    while startday <= endday:
        daylist.append(startday)
        startday = startday + datetime.timedelta(days=1)
    return daylist


def main(someday):
    day = int(someday.strftime("%Y%m%d"))
    objs = list(News.query.get_by_day(day))
    total_content = u""
    for o in objs:
        keyword = get_keyword(o.content)
        o.keyword = keyword
        db.session.add(o)
        #print keyword
        total_content += o.content
    keyword = get_keyword(total_content, 20)
    #print keyword
    objs[0].keyword = keyword
    db.session.add(objs[0])
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


