__author__ = 'zhouzhiming'


import tornado.web
import os
import logging

class ResourceHandler(tornado.web.RequestHandler):
    def get(self):
        path = os.path.join('res', self.request.uri.strip('/').replace('/', os.path.sep))
        content = open(path, 'rb').read()
        content_type = None
        if path.endswith('.png'):
            content_type = 'image/png'
        if content_type:
            self.set_header('Content-Type', content_type)
        logging.info("ResHandler: path=%s, content_type=%s, content size=%d"
                     % (path, content_type, len(content)))
        self.write(content)

