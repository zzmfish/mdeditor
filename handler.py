# encoding=utf-8

import os
import json
import tornado.web

import config
import utils
import tools.make_html


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        utils.check_ip(self.request)
        files = os.listdir(config.md_dir)
        md_files = []
        for fn in files:
            if fn.endswith('.md'):
                md_files.append(fn[ : fn.rfind('.')])
        md_files.sort()
        self.render('main.html', files=json.dumps(md_files))


class RenderHandler(tornado.web.RequestHandler):
    def post(self):
        utils.check_ip(self.request)
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


from file_handler import GetFileHandler, SaveFileHandler
