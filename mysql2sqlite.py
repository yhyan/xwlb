#coding:utf-8

import datetime
import MySQLdb

DB = None
C = None


def get_objs():
    sql = """select num, day, url, title, keyword, content from news_xwlb"""
    C.execute(sql)
    return C.fetchall()


def init_db(host="localhost", charset="utf8"):
    global DB, C

    DB = MySQLdb.connect(user='dbuser', passwd="dbpasswd", db="dbname", host=host, charset=charset)
    C = DB.cursor()


def close_db():
    global DB, C

    C.close()
    DB.close()

init_db()

from models import News, db
db.create_all()

def main():
    objs = get_objs()
    print(len(objs))
    print(objs[0])
    for o in objs:
        num = o[0]
        day = int(o[1].strftime("%Y%m%d"))
        url = o[2]
        title = o[3]
        keyword = o[4]
        content = o[5]
        id = day * 100 + num

        t = News.query.filter(News.id == id).first()
        if not t:
            n = News(
                id=id,
                num=num,
                day=day,
                url=url,
                title=title,
                keyword=keyword,
                content=content)
            db.session.add(n)
        else:
            t.num = num
            t.day = day
            t.url = url
            t.title = title
            t.keyword = keyword
            t.content = content
            t.updated_at = datetime.datetime.now()
            db.session.add(t)
    db.session.commit()



if __name__ == "__main__":
    main()
