#!/usr/bin/python
#encoding=utf-8

import sys
import logging
sys.path.insert(0, './external/tornado')
import tornado.ioloop
import tornado.web
import tornado.log

import config
import handler


def main():
    html_dir = config.html_dir
    if type(html_dir) is str:
        html_dir = html_dir.decode(config.fs_charset)

    tornado.log.enable_pretty_logging()
    application = tornado.web.Application(
        [
            (r"/", handler.MainHandler),
            (r"/GetFile", handler.GetFileHandler),
            (r"/SaveFile", handler.SaveFileHandler),
            (r"/list", handler.ListFilesHandler),
            (r"/move", handler.MoveFileHandler),
            (r"/Render", handler.RenderHandler),
            (r"/css/.*", handler.ResourceHandler),
            (r"/js/.*", handler.ResourceHandler),
            (r"/lib/.*", handler.ResourceHandler),
            (r"/(images/.*)", tornado.web.StaticFileHandler, {"path": html_dir}),
        ],
        static_path='.'
    )
    application.listen(config.port)
    logging.info('start at port %d' % config.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

