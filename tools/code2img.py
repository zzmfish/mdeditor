#encoding=utf-8
#内置库
import re
import subprocess
import base64
#第三方库
import markdown
#自定义
import config

class Code2ImgPreprocessor(markdown.preprocessors.Preprocessor):
    def uml(self, code):
        pipe = subprocess.Popen(['java', '-jar', config.plantuml_path, '-pipe', '-tpng'], \
                stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        if type(code) is unicode:
            code = code.encode('utf-8')
        pipe.stdin.write(code)
        pipe.stdin.close()
        return pipe.stdout.read()
        
    def run(self, lines):
        text = '\n'.join(lines)
        print text
        regx = re.compile(r'```(uml)\b(.*?)```', re.MULTILINE | re.DOTALL)
        while True:
            match = regx.search(text)
            if not match:
                break
            img_type = match.group(1)
            img_code = match.group(2)
            img_data = ''
            if img_type == 'uml':
                img_data = self.uml(img_code)
            text = text.replace(match.group(0), '<img src="data:image/png;base64,%s" />' % base64.b64encode(img_data))

        return text.split('\n')

class Code2Img(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('code2img',
                Code2ImgPreprocessor(), "<fenced_code_block")

def makeExtension(*args, **kwargs):
    return Code2Img(*args, **kwargs)
