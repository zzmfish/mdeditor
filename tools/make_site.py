# encoding=utf-8
import sys
import os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config
import make_html

links = []
for root, dirs, files in os.walk(config.md_dir, followlinks=False):
    for file_name in files:
        if not file_name.endswith('.md'):
            continue
        md_file = os.path.join(root, file_name)
        html_file = os.path.join(root, file_name[:-3] + '.html')
        should_make_html = False
        if os.path.exists(html_file):
            md_mtime = os.stat(md_file).st_mtime
            html_mtime = os.stat(html_file).st_mtime
            if md_mtime > html_mtime:
                should_make_html = True
        else:
            should_make_html = True

        if should_make_html:
            print '%s' % md_file
            print '  -> %s' % html_file
            html = make_html.make_html(open(md_file, 'r').read(), 'style.css')
            open(html_file, 'w').write(html)

        rel_path = html_file
        if rel_path.startswith(config.html_dir):
            rel_path = rel_path[len(config.html_dir):]
        links.append(rel_path.strip(os.path.sep))

index_path = os.path.join(config.html_dir, 'index.html')
print 'writing %s' % index_path
index_file = open(index_path, 'w')
index_file.write('<html><head>')
index_file.write('<title>%s</title>' % config.title)
index_file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
index_file.write('</head>')
index_file.write('<body>')
index_file.write('<h1>%s</h1>' % config.title)
index_file.write('<ul>')
for link in links:
    index_file.write('<li><a href="%s">%s</a></li>' % (link, link[:-5]))
index_file.write('</ul>')
index_file.write('</body></html>')
index_file.close()

