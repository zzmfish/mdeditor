# encoding=utf-8
import os
import sys

cur_dir = os.path.dirname(__file__)
top_dir = os.path.join(cur_dir, '..')
top_dir = os.path.abspath(top_dir)
os.chdir(top_dir)
sys.path.append(top_dir)

import config
import make_html

reload(sys)
sys.setdefaultencoding(config.fs_charset)

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
            html = make_html.make_html(open(md_file, 'r').read(), '/style.css')
            open(html_file, 'w').write(html)

        rel_path = html_file
        if rel_path.startswith(config.html_dir):
            rel_path = rel_path[len(config.html_dir):]
        links.append(rel_path.strip(os.path.sep))

files = [link[:-5] for link in links]
print '\n'.join(files)
index_path = os.path.join(config.html_dir, 'index.html')
print 'writing %s' % index_path
index_file = open(index_path, 'w')
index_file.write('<html><head>')
index_file.write('<title>%s</title>' % config.title)
index_file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
index_file.write('''
<link rel="stylesheet" href="res/jstree/themes/default/style.min.css" />
<script src="res/jquery.js" type="text/javascript" charset="utf-8"></script>
<script src="res/file_browser.js" type="text/javascript" charset="utf-8"></script>
<script src="res/jstree/jstree.js" type="text/javascript" charset="utf-8"></script>
''')

index_file.write('</head>')
index_file.write('<body style="padding:0px; margin: 0px;">')

index_file.write('''
<table style="width:100%; height:100%">
    <tr>
        <td style="vertical-align:top; width:20%; background-color: rgb(232, 233, 232);">
            <div>搜索：<input type=text id="SearchInput" /></div>
            <div id="FileBrowser" style="width:100%;"></div>
        </td>
        <td>
            <iframe id="PageFrame" style="width:100%;height:100%;" frameborder="0" ></iframe>
        </td>
    </tr>
</table>
''');
index_file.write("""
<script>
FileBrowser.update(["%s"]);
FileBrowser.onOpen = function(filePath) {
    document.getElementById('PageFrame').src = filePath + '.html';
}
var searchTimeout = undefined;
$('#SearchInput').keyup(function () {
    if(searchTimeout)
        clearTimeout(searchTimeout);
	searchTimeout = setTimeout(function () {
        var v = $('#SearchInput').val();
        FileBrowser.search(v);
    }, 250);
});

</script>
""" % '","'.join(files))
index_file.write('</body></html>')
index_file.close()

res_dir = os.path.join(config.html_dir, 'res')
if not os.path.exists(res_dir):
    os.mkdir(res_dir)
os.system('cp -rv res/lib/jquery.js %s/' % res_dir)
os.system('cp -rv res/lib/jstree %s/' % res_dir)
os.system('cp -rv res/js/file_browser.js %s/' % res_dir)
