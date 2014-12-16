__author__ = 'zhouzhiming'

import json
import tornado.web

import utils
import file_manager


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        utils.check_ip(self.request)
        file_names = file_manager.file_manager.get_file_names()
        self.render('main.html', files=json.dumps(file_names))


