# encoding=utf-8
__author__ = 'zhouzhiming'

import os
import json
import tornado.web
import tornado.log
import utils
import config
from file_manager import file_manager


def execute_shell(cmd):
    tornado.log.app_log.info(cmd)
    os.system(cmd)


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
        files = utils.list_files(config.md_dir, '.md')
        self.write(json.dumps(files, indent=2))


class MoveFileHandler(tornado.web.RequestHandler):
    def get(self):
        from_name = self.get_argument('from').encode(config.fs_charset)
        to_name = self.get_argument('to').encode(config.fs_charset)

        if os.path.exists(os.path.join(config.md_dir, from_name)):
            execute_shell('cd %s; git mv "%s" "%s"' % (config.md_dir, from_name, to_name))
            execute_shell('cd %s; mv "%s" "%s"' % (config.md_dir, from_name, to_name))
        if os.path.exists(os.path.join(config.md_dir, from_name + '.md')):
            execute_shell('cd %s; git mv "%s.md" "%s.md"' % (config.md_dir, from_name, to_name))
            execute_shell('cd %s; mv "%s.md" "%s.md"' % (config.md_dir, from_name, to_name))


class MkDirHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name').encode(config.fs_charset)

        #execute_shell('cd %s; git add "%s"' % (config.md_dir, name))

        path = os.path.join(config.md_dir, name)
        tornado.log.app_log.info('mkdir %s' % path)
        os.mkdir(path)


class TouchHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name').encode(config.fs_charset)

        path = os.path.join(config.md_dir, name)
        tornado.log.app_log.info('touch %s' % path)
        open(path, 'w').close()

        #execute_shell('cd %s; git add "%s"' % (config.md_dir, name))


class RemoveHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name').encode(config.fs_charset)

        path = os.path.join(config.md_dir, name)
        tornado.log.app_log.info('remove %s' % path)

        if os.path.exists(os.path.join(config.md_dir, name)):
            execute_shell('cd %s; git rm -f "%s"' % (config.md_dir, name))
        if os.path.exists(os.path.join(config.md_dir, name)):
            execute_shell('cd %s; rmdir "%s"' % (config.md_dir, name))
        if os.path.exists(os.path.join(config.md_dir, name + '.md')):
            execute_shell('cd %s; git rm -f "%s"' % (config.md_dir, name + '.md'))
        if os.path.exists(os.path.join(config.md_dir, name + '.md')):
            execute_shell('cd %s; rm "%s"' % (config.md_dir, name + '.md'))

