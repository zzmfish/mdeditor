
var Editor = {
    fileName : null,
    editor : null,

    init : function()
    {
        //初始化编辑器
        var editor = ace.edit("Editor");
        editor.setTheme("ace/theme/chaos");
        editor.renderer.setOption('showLineNumbers', false);
        editor.renderer.setOption('showGutter', false);
        editor.renderer.setOption('showPrintMargin', false);
        editor.getSession().setUseWrapMode(true);
        editor.on("change", OnContentChange);

        //设置markdown模式
        var MarkdownMode = require("ace/mode/markdown").Mode;
        editor.getSession().setMode(new MarkdownMode());

        this.editor = editor;
    },

    getValue : function()
    {
        return this.editor.getValue();
    },

    setValue : function(value)
    {
        this.editor.setValue(value);
        this.editor.clearSelection();
        this.editor.gotoLine(0);
    },

    update : function() {
        this.editor.renderer.updateFull(true);
    },

    focus : function()
    {
        this.editor.focus();
    },

    changeTheme : function()
    {
        var themeName = document.getElementById('ThemeSelect').value;
        this.editor.setTheme("ace/theme/" + themeName);
    },


    editFile : function(fileName)
    {
        debug('EditFile(' + fileName + ')');
        ConfirmUnsavedFile();
        Editor._updateFileName(fileName);

        //发起http请求：获取markdown文件内容
        var req = new XMLHttpRequest();
        req.open('GET', '/GetFile?f=' + encodeURIComponent(fileName), true);
        req.onreadystatechange = function() {
            if (req.readyState == 4 && req.status == 200) {
                //得到文件内容，并设置到编辑器
                Editor.setValue(req.responseText, -1);
                Editor.focus();
                document.getElementById('EditorContainer').style.display = '';
                document.getElementById('SaveButton').setAttribute('disabled', '');
                gNeedRendering = true;
                Render();
            }
        }
        req.send();
    },

    _updateFileName : function(fileName)
    {
        this.fileName = fileName;
        location.hash = escape(fileName);
        document.title = fileName + ' - MDEditor';
    },

    GetFileName : function()
    {
        return this.fileName;
    },


    SaveFile : function()
    {
        var fileName = Editor.GetFileName();
        if (!fileName)
            return;
        //发起http请求：保存文件
        var req_content = 'text=' + encodeURIComponent(Editor.getValue())
                + '&f=' + encodeURIComponent(fileName);
        var req = new XMLHttpRequest();
        req.open('POST', '/SaveFile', false);
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.setRequestHeader("Content-length", req_content.length);
        req.send(req_content);

        //显示保存成功或失败
        var statusElem = document.getElementById('Status');
        if (req.status == 200) {
            statusElem.textContent = '文件保存成功！';
            document.getElementById('SaveButton').setAttribute('disabled', '');
        }
        else
            statusElem.textContent = '文件保存失败！';

        //取消显示
        setTimeout(function() {
            statusElem.textContent = '';
        }, 3000);
    }


};
