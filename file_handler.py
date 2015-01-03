__author__ = 'zhouzhiming'

import tornado.web
import utils
from file_manager import file_manager

class GetFileHandler(tornado.web.RequestHandler):
    def get(self):
        utils.check_ip(self.request)
        name = self.get_argument('f')
        text = file_manager.load_file(name) or ''
        self.write(text)

class SaveFileHandler(tornado.web.RequestHandler):
    def post(self):
        utils.check_ip(self.request)
        text = self.get_body_argument('text')
        name = self.get_body_argument('f')
        file_manager.save_file(name, text)
        self.write('OK')

