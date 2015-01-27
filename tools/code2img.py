#encoding=utf-8
#内置库
import re
import subprocess
import base64
#第三方库
import markdown
#自定义
import config

class LRUCache:
    def __init__(self, size=10):
        self.cache = []
        self.size = size

    def load_data(self, key):
        for i in range(len(self.cache)):
            item = self.cache[i]
            if item[0] == key:
                # 如果命中则添加到列表最后，然后返回
                del self.cache[i]
                self.cache.append(item)
                return item[1]
        return None

    def save_data(self, key, value):
        while len(self.cache) >= self.size:
            del self.cache[0]
        self.cache.append((key, value))

class Code2ImgPreprocessor(markdown.preprocessors.Preprocessor):
    data_cache = LRUCache()

    def uml(self, code):
        pipe = subprocess.Popen(['java', '-jar', config.plantuml_path, '-pipe', '-tpng'], \
                stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        if type(code) is unicode:
            code = code.encode('utf-8')
        pipe.stdin.write(code)
        pipe.stdin.close()
        return pipe.stdout.read()

    def dot(self, code):
        pipe = subprocess.Popen(['dot', '-Tpng'], \
                stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        if type(code) is unicode:
            code = code.encode('utf-8')
        pipe.stdin.write(code)
        pipe.stdin.close()
        return pipe.stdout.read()
        
    def run(self, lines):
        text = '\n'.join(lines)
        regx = re.compile(r'```[\r\n]*(uml|dot)\b(.*?)```', re.MULTILINE | re.DOTALL)
        while True:
            match = regx.search(text)
            if not match:
                break
            img_data = self.data_cache.load_data(match.group(0))
            if not img_data:
                img_type = match.group(1)
                img_code = match.group(2)
                img_data = ''
                if img_type == 'uml':
                    img_data = self.uml(img_code)
                elif img_type == 'dot':
                    img_data = self.dot(img_code)
                if img_data:
                    self.data_cache.save_data(match.group(0), img_data)
            text = text.replace(match.group(0), '<img src="data:image/png;base64,%s" />' % base64.b64encode(img_data))

        return text.split('\n')

class Code2Img(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('code2img',
                Code2ImgPreprocessor(), "<fenced_code_block")

def makeExtension(*args, **kwargs):
    return Code2Img(*args, **kwargs)
