# encoding=utf-8
import os
import config


class FileManager:

    def __init__(self):
        self.file_dir = config.md_dir

    def get_file_names(self):
        out_names = []
        file_names = os.listdir(self.file_dir)
        for file_name in file_names:
            if file_name.endswith('.md'):
                out_names.append(file_name[ : file_name.rfind('.')])
        return out_names

file_manager = FileManager()
