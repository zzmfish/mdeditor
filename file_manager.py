# encoding=utf-8
import os
import config
import tornado.log


class FileManager:

    def __init__(self):
        self.file_dir = config.md_dir

    def get_file_names(self):
        # 递归子目录，列出md文件
        out_names = []
        for root, dirs, files in os.walk(self.file_dir, followlinks=True):
            # 不显示起始目录
            if root.startswith(self.file_dir):
                root = root[len(self.file_dir):]
            root = root.strip(os.sep)
            for file_name in files:
                # 只显示md文件，但不显示扩展名
                if file_name.endswith('.md'):
                    display_name = file_name[ : file_name.rfind('.')]
                    out_names.append(os.path.join(root, display_name))

        return out_names

    def __get_file_path(self, name):
        #if type(name) is unicode:
        #    name = name.encode(config.fs_charset)
        return os.path.join(config.md_dir, '%s.md' % name)

    def save_file(self, name, data):
        if not name:
            return False
        file_path = self.__get_file_path(name)
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        tornado.log.app_log.info('file %s is saved, size is %d' % (file_path, len(data)))
        open(file_path, 'w').write(data)
        return True

    def load_file(self, name):
        if not name:
            return False
        file_path = self.__get_file_path(name)
        if not os.path.exists(file_path):
            return False
        data = open(file_path, 'r').read()
        tornado.log.app_log.info('file %s is loaded, size is %d' % (file_path, len(data)))
        return data

file_manager = FileManager()
