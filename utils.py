# encoding=utf-8
import os

def check_ip(request):
    if request.remote_ip not in ['127.0.0.1', '10.0.2.2']:
        raise Exception('unauthorized ip')


def list_files(root_dir, format):
    result = {}
    exclude_dirs = ['.git', 'images', 'res']
    for root, dirs, files in os.walk(root_dir, followlinks=True):
        if root.startswith('.') or root.find('/.') >= 0:
            continue
        # 不显示起始目录
        if root.startswith(root_dir):
            root = root[len(root_dir):]
        root = root.strip(os.sep)

        # 跳过特殊目录
        should_skip = False
        for exclude_dir in exclude_dirs:
            if root == exclude_dir or root.startswith(exclude_dir + os.sep):
                should_skip = True
        if should_skip:
            continue

        # 记录上层目录
        parent_dir = result
        for depth in root.split(os.sep):
            if len(depth) == 0:
                break
            if depth not in parent_dir:
                parent_dir[depth] = {}
            parent_dir = parent_dir[depth]

        # 记录子目录
        for sub_dir in dirs:
            if not sub_dir.startswith('.') and sub_dir not in exclude_dirs:
                parent_dir[sub_dir] = {}

        # 记录文件
        for file in files:
            if file.endswith(format):
                #parent_dir[file[:-len(format)]] = None
                parent_dir[file] = None

    return result
