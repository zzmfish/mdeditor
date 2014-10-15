
md_dir = '.'
html_dir = '.'
port = 8889

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'md_dir':
        print md_dir
    elif sys.argv[1] == 'html_dir':
        print html_dir
