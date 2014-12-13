__author__ = 'zhouzhiming'

import os
import json
import tornado.web

import utils
import config


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


