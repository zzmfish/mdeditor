
var Toolbar = {
    files : [],
    init : function(files) {
        this.setFiles(files);

        //获取控件
        this.fileNameInput = $("#FileNameInput");
        this.showSourceInput = $('#ShowSource');
        this.showRendererInput = $('#ShowRenderer');

        //输入框自动完成
        this.fileNameInput.autocomplete({
            source: Toolbar.files,
            minLength: 0,
            delay: 100,
            select: function(e, ui) {
                Editor.editFile(ui.item.value);
            }
        }).click(function() {
            $(this).autocomplete('search', $(this).val());
        }).keydown(function(e){
            var key = e.which;
            if (key == 13) {
                var value = $(this).val();
                if (Toolbar.files.indexOf(value) == -1) {
                    Toolbar.addFile(value);
                }
                Editor.editFile(value);
            }
        }).blur(function(e) {
            $(this).val(Editor.GetFileName());
        });

        //显示源码
        this.showSourceInput.change(function() {
            if (!Toolbar.showRendererInput.prop('checked'))
                $(this).prop('checked', true);
            Toolbar._updateSourceAndRendererLayout();
        });

        //显示渲染
        this.showRendererInput.change(function() {
            if (!Toolbar.showSourceInput.prop('checked'))
                $(this).prop('checked', true);
            Toolbar._updateSourceAndRendererLayout();
        });

        //根据url hash打开文件
        if (window.location.hash) {
            var fileName = unescape(window.location.hash.substr(1));
            this.fileNameInput.val(fileName);
            Editor.editFile(fileName);
        }

    },
    addFile : function(name)
    {
        var files = this.files;
        files.push(name);
        this.setFiles(files);
    },
    setFiles : function(files)
    {
        //获取文件列表
        this.files = files;
        this.files.sort(function (a, b) {
            return a.toLowerCase().localeCompare(b.toLowerCase());
         });
    },
    _updateSourceAndRendererLayout : function()
    {
        var showSource = this.showSourceInput.prop('checked');
        var showRenderer = this.showRendererInput.prop('checked');
        if (showSource && showRenderer) {
            $('#EditorTd').css('width', '50%').css('display', '');
            $('#RendererTd').css('width', '50%').css('display', '');
        }
        else if (showSource) {
            $('#EditorTd').css('width', '100%').css('display', '');
            $('#RendererTd').css('width', '0%').css('display', 'none');
        }
        else if (showRenderer) {
            $('#EditorTd').css('width', '0%').css('display', 'none');
            $('#RendererTd').css('width', '100%').css('display', '');
        }
    }
};
