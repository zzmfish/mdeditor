# encoding=utf-8
import os
import sys
import json

cur_dir = os.path.dirname(__file__)
top_dir = os.path.join(cur_dir, '..')
top_dir = os.path.abspath(top_dir)
os.chdir(top_dir)
sys.path.append(top_dir)

import config
import utils

reload(sys)
sys.setdefaultencoding(config.fs_charset)

files = utils.list_files(config.html_dir, '.html')

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
FileBrowser.update(%s);
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
""" % json.dumps(files))
index_file.write('</body></html>')
index_file.close()

res_dir = os.path.join(config.html_dir, 'res')
if not os.path.exists(res_dir):
    os.mkdir(res_dir)
os.system('cp -rv res/lib/jquery.js %s/' % res_dir)
os.system('cp -rv res/lib/jstree %s/' % res_dir)
os.system('cp -rv res/js/file_browser.js %s/' % res_dir)
