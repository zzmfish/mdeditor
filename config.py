#encoding=utf-8
port = 8889
md_dir = '.'
html_dir = '.'
plantuml_path = './plantuml.jar'

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'md_dir':
        print md_dir
    elif sys.argv[1] == 'html_dir':
        print html_dir
