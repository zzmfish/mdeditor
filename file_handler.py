# encoding=utf-8
__author__ = 'zhouzhiming'

import os
import json
import tornado.web
import utils
import config
from file_manager import file_manager


class GetFileHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        utils.check_ip(self.request)
        name = self.get_argument('f')
        if name.startswith('/') or name.find('..') >= 0:
            return
        text = file_manager.load_file(name) or ''
        self.write(text)


class SaveFileHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        utils.check_ip(self.request)
        text = self.get_body_argument('text')
        name = self.get_body_argument('f')
        file_manager.save_file(name, text)
        self.write('OK')


class ListFilesHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        result = {}
        root_dir = config.md_dir
        for root, dirs, files in os.walk(root_dir, followlinks=True):
            # 不显示起始目录
            if root.startswith(root_dir):
                root = root[len(root_dir):]
            root = root.strip(os.sep)

            # 跳过特殊目录
            should_skip = False
            for exclude_dir in ['.git', 'images', 'res']:
                if root == exclude_dir or root.startswith(exclude_dir + os.sep):
                    should_skip = True
            if should_skip:
                continue

            # 记录上层目录
            parent_dir = result
            for depth in root.split(os.sep):
                if depth not in parent_dir:
                    parent_dir[depth] = {}
                parent_dir = parent_dir[depth]

            # 记录子目录
            for sub_dir in dirs:
                parent_dir[sub_dir] = {}

            # 记录文件
            for file in files:
                parent_dir[file] = None


        self.write(json.dumps(result, indent=2))
