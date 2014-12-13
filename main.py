#!/usr/bin/python
#encoding=utf-8

import sys
sys.path.insert(0, './external/tornado')
import tornado.ioloop
import tornado.web
import tornado.log

import config
import handler


def main():
    tornado.log.enable_pretty_logging()
    application = tornado.web.Application([
        (r"/", handler.MainHandler),
        (r"/GetFile", handler.GetFileHandler),
        (r"/SaveFile", handler.SaveFileHandler),
        (r"/Render", handler.RenderHandler),
        (r"/css/.*", handler.ResourceHandler),
        (r"/js/.*", handler.ResourceHandler),
        (r"/lib/.*", handler.ResourceHandler),
    ])
    application.listen(config.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

