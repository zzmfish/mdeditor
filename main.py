#!/usr/bin/python
#encoding=utf-8
import base64
import json
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
            if fn.endswith('.md'):
                md_files.append(fn[ : fn.rfind('.')])
        md_files.sort()
        self.render('main.html', files=json.dumps(md_files))

class GetFileHandler(tornado.web.RequestHandler):
    def get(self):
        check_ip(self.request)
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
        check_ip(self.request)
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

