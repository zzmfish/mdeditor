__author__ = 'zhouzhiming'

import os
import tornado.web

import config
import utils

class GetFileHandler(tornado.web.RequestHandler):
    def get(self):
        utils.check_ip(self.request)
        f = self.get_argument('f')
        text = ''
        if f:
            f += '.md'
            try:
                text = open(os.path.join(config.md_dir, f), 'r').read()
            except IOError:
                pass
        print 'file %s is loaded, size is %d' % (f, len(text))
        self.write(text)

class SaveFileHandler(tornado.web.RequestHandler):
    def post(self):
        utils.check_ip(self.request)
        text = self.get_body_argument('text')
        f = self.get_body_argument('f')
        if not f:
            return
        f += '.md'
        f = os.path.join(config.md_dir, f)
        data = text.encode('utf-8')
        open(f, 'w').write(data)
        print 'file %s is saved, size is %d' % (f, len(data))
        self.write('OK')

