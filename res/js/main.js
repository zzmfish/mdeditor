var gIsRendering = false;
var gNeedRendering = false;

function debug(msg)
{
    console.log(msg);
}

function NeedSaveFile()
{
    return ! document.getElementById('SaveButton').hasAttribute('disabled')
            && Editor.getValue();
}

function ConfirmUnsavedFile()
{
    if (NeedSaveFile() && confirm("是否保存文件？"))
        Editor.SaveFile();
}

function Render()
{
    if (!gNeedRendering) return;
    if (gIsRendering) return;
    gIsRendering = true;

    //发起http请求：把markdown渲染成html
    var req_content = 'text=' + encodeURIComponent(Editor.getValue());
    var req = new XMLHttpRequest();
    req.open('POST', '/Render', true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.setRequestHeader("Content-length", req_content.length);
    req.setRequestHeader("Connection", "close");
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            if (req.status == 200) {
                //得到子文档对象
                var renderer = document.getElementById('Renderer');
                var wnd = renderer.contentWindow;
                var doc = wnd.document;

                //得到子文档滚动位置
                var docY = wnd.scrollY;
                var maxY = doc.height - wnd.innerHeight;
                console.log('Render: docY=' + docY + ', maxY=' + maxY);

                //在子文档显示渲染的html
                doc.open();
                doc.write(req.responseText);

                //定位到末尾
                renderer.onload = function() {
                    if (maxY > 0 && docY >= maxY) {
                        wnd.scrollTo(0, 9999);
                    }
                    else {
                        wnd.scrollTo(0, docY);
                    }
                }
                doc.close(); //触发onload
            }
            gIsRendering = false;
            gNeedRendering = false;
        }
    }
    req.send(req_content);
}

function OnContentChange()
{
    document.getElementById('SaveButton').removeAttribute('disabled');
    document.getElementById('Status').textContent = '';
    gNeedRendering = true;
    setTimeout(Render, 1500);
}


//var files = {% raw files %};
Editor.init();
Toolbar.init([]);
FileBrowser.onOpen = function(filePath) {
    document.getElementById('FileNameInput').value = filePath;
    Editor.editFile(filePath);
};

FileBrowser.onMove = function(oldPath, newPath) {
    if (oldPath != newPath)
        FileManager.move(oldPath, newPath);
};

FileBrowser.onCreateFolder = function(path) {
    FileManager.createFolder(path);
};

FileBrowser.onCreateFile = function(path) {
    FileManager.createFile(path);
};

FileBrowser.onDelete = function(path) {
    FileManager.remove(path);
};



var fileName = null;
//根据url hash打开文件
if (window.location.hash) {
    fileName = unescape(window.location.hash.substr(1));
    Toolbar.fileNameInput.val(fileName);
    Editor.editFile(fileName);
    //FileBrowser.select(fileName);
}

FileBrowser.update(undefined, fileName);

window.onbeforeunload = function() {
    if (NeedSaveFile())
        return "文档没保存，是否离开？"
}