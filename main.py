#!/usr/bin/env python

import urllib
import datetime

import tornado.escape
import tornado.ioloop
import tornado.web
import os.path

from tornado import httpserver
from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line
from tornado import template


from models import News, db


define("port", default=8880, help="run on the given port", type=int)


def to_int(d):
    return int(d.strftime("%Y%m%d"))

class MainHandler(tornado.web.RequestHandler):

    def on_finish(self):
        db.session.remove()

    def get_detail_page(self):
        try:
            day = datetime.datetime.strptime(
                self.get_argument('day'), '%Y%m%d')
        except:
            day = datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        next_day = day + datetime.timedelta(days=1)
        prev_day = day - datetime.timedelta(days=1)
        uri = self.request.uri[0:self.request.uri.find("?")]
        next_url = uri + "?day=%s" % next_day.strftime("%Y%m%d")
        prev_url = uri + "?day=%s" % prev_day.strftime("%Y%m%d")
        if not News.query.exist(to_int(next_day)):
            next_url = None
        if not News.query.exist(to_int(prev_day)):
            prev_url = None
        news = News.query.get_by_day(to_int(day))
        self.render('detail.html', news=news,
                    next_url=next_url, prev_url=prev_url)

    def get_index_page(self):
        page = int(self.get_argument('page', 1))
        page_obj = News.query.index_page().paginate(
            page=page, per_page=News.PER_PAGE)
        page_url = lambda page: self.request.uri[
            :self.request.uri.find("?")] + "?%s" % urllib.urlencode(dict(page=page))
        self.render('index.html', page_obj=page_obj, page_url=page_url)

    def get(self, *args):
        if len(args) >= 1:
            api_or_page = args[0]
        else:
            api_or_page = ''
        if api_or_page == 'detail':
            self.get_detail_page()
        else:
            self.get_index_page()


def main():
    tornado.options.parse_command_line()
    settings = dict(
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "html"),
        static_path=os.path.join(os.path.dirname(__file__), "html"),
        xsrf_cookies=True,
        debug=False,
    )

    mapping = [
        (r"/(.*)?", MainHandler),
    ]
    app = tornado.web.Application(
        mapping, **settings
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
