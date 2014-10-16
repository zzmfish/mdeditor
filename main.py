#!/usr/bin/python
#encoding=utf-8
import base64
import os
import os.path
import tools.make_html
import config

import sys
sys.path.insert(0, './external/tornado')
import tornado.ioloop
import tornado.web

def check_ip(request):
    if request.remote_ip != '127.0.0.1':
        raise Exception('unauthorized ip')
    
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        check_ip(self.request)
        files = os.listdir(config.md_dir)
        md_files = []
        for fn in files:
            if fn.endswith('.md') or fn.endswith('.mkd') or fn.endswith('.markdown'):
                md_files.append(fn)
        md_files.sort()
        self.render('main.html', files=md_files)

class GetFileHandler(tornado.web.RequestHandler):
    def get(self):
        check_ip(self.request)
        f = self.get_argument('f')
        text = ''
        if f:
            text = open(os.path.join(config.md_dir, f), 'r').read()
        self.write(text)
       
class SaveFileHandler(tornado.web.RequestHandler):
    def post(self):
        check_ip(self.request)
        text = self.get_body_argument('text')
        f = self.get_body_argument('f')
        f = os.path.join(config.md_dir, f)
        open(f, 'w').write(text.encode('utf-8'))
        self.write('OK')
 
class RenderHandler(tornado.web.RequestHandler):
    def post(self):
        check_ip(self.request)
        text = self.get_body_argument('text')
        css = open('style.css', 'r').read()
        html = tools.make_html.make_html(text, css)
        #html = base64.b64encode(html)
        self.write(html)
        
class ResourceHandler(tornado.web.RequestHandler):
    def get(self):
        path = self.request.uri.strip('/')
        content = open(os.path.join('./res', path), 'r').read()
        self.write(content)
        
from tornado.log import enable_pretty_logging
enable_pretty_logging()
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/GetFile", GetFileHandler),
    (r"/SaveFile", SaveFileHandler),
    (r"/Render", RenderHandler),
    (r"/css/.*", ResourceHandler),
    (r"/js/.*", ResourceHandler),
    (r"/lib/.*", ResourceHandler),
])
application.listen(config.port)
tornado.ioloop.IOLoop.instance().start()

