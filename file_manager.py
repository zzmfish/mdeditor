# encoding=utf-8
import os
import config


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

    def save_file(self, name, data):
        if not name:
            return False
        path = os.path.join(config.md_dir, '%s.md' % name)
        os.makedirs(os.path.dirname(path))
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        print 'file %s is saved, size is %d' % (path, len(data))
        open(path, 'w').write(data)
        return True

file_manager = FileManager()
