
var Toolbar = {
    files : [],
    init : function(files) {
        Toolbar._log('init');
        this.setFiles(files);

        //获取控件
        this.fileNameInput = $("#FileNameInput");
        this.showSourceInput = $('#ShowSource');
        this.showRendererInput = $('#ShowRenderer');
        this.showFileBrowserInput = $('#ShowFileBrowser');

        //输入框自动完成
        this.fileNameInput.autocomplete({
            source: Toolbar.files,
            minLength: 0,
            delay: 100,
            select: function(e, ui) {
                Toolbar._log('FileNameInput.select: ' + ui.item.value);
                Editor.editFile(ui.item.value);
            }
        }).click(function() {
            Toolbar._log('FileNameInput.click');
            $(this).autocomplete('search', $(this).val());
        }).keydown(function(e){
            Toolbar._log('FileNameInput.keydown');
            var key = e.which;
            if (key == 13) {
                var value = $(this).val();
                if (Toolbar.files.indexOf(value) == -1) {
                    Toolbar.addFile(value);
                }
                Editor.editFile(value);
            }
        }).blur(function(e) {
            Toolbar._log('FileNameInput.blur');
            $(this).val(Editor.GetFileName());
        });

        //显示源码
        this.showSourceInput.change(function() {
            Toolbar._log('ShowSource.change');
            if (!Toolbar.showRendererInput.prop('checked'))
                $(this).prop('checked', true);
            Toolbar._updateSourceAndRendererLayout();
        });

        //显示渲染
        this.showRendererInput.change(function() {
            Toolbar._log('ShowRender.change');
            if (!Toolbar.showSourceInput.prop('checked'))
                $(this).prop('checked', true);
            Toolbar._updateSourceAndRendererLayout();
        });

        this.showFileBrowserInput.change(function() {
            Toolbar._log('ShowFileBrowser.change');
            Toolbar._updateSourceAndRendererLayout();
        });

        //根据url hash打开文件
        if (window.location.hash) {
            var fileName = unescape(window.location.hash.substr(1));
            this.fileNameInput.val(fileName);
            Editor.editFile(fileName);
        }

        Toolbar._updateSourceAndRendererLayout()
    },
    addFile : function(name)
    {
        Toolbar._log('addFile: ' + name);
        var files = this.files;
        files.push(name);
        this.setFiles(files);
    },
    setFiles : function(files)
    {
        Toolbar._log('setFiles');
        //获取文件列表
        this.files = files;
        this.files.sort(function (a, b) {
            return a.toLowerCase().localeCompare(b.toLowerCase());
         });
    },
    _updateSourceAndRendererLayout : function()
    {
        Toolbar._log('_updateSourceAndRendererLayout');
        var showSource = this.showSourceInput.prop('checked');
        var showRenderer = this.showRendererInput.prop('checked');
        var showFileBrowser = this.showFileBrowserInput.prop('checked');
        var restWidth = 100;
        if (showFileBrowser) {
            $('#FileBrowserTd').css('width', '20%').css('display', '');
            restWidth -= 20;
        }
        else
            $('#FileBrowserTd').css('width', '20%').css('display', 'none');

        if (showSource && showRenderer) {
            $('#EditorTd').css('width', restWidth / 2 + '%').css('display', '');
            $('#RendererTd').css('width', restWidth / 2 + '%').css('display', '');
        }
        else if (showSource) {
            $('#EditorTd').css('width', restWidth + '%').css('display', '');
            $('#RendererTd').css('width', '0%').css('display', 'none');
        }
        else if (showRenderer) {
            $('#EditorTd').css('width', '0%').css('display', 'none');
            $('#RendererTd').css('width', restWidth + '%').css('display', '');
        }
    },
    _log : function(msg)
    {
        console.log('Toolbar# ' + msg);
    }
};
