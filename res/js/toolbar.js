
var Toolbar = {
    files : [],
    init : function(files) {
        Toolbar._log('init');
        this.setFiles(files);

        //获取控件
        this.fileNameInput = $("#FileNameInput");
        this.showSourceInput = $('#ShowSource');
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

        Toolbar.switchLayout('browse');
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
    switchLayout : function(mode)
    {
        //更新设置
        var showRenderer = true;
        if (mode == 'browse') {
            $('#FileBrowserTd').css('width', Math.floor(0.2 * window.innerWidth) + 'px').css('display', '');
            $('#FileBrowser').css('width', Math.floor(0.2 * window.innerWidth) + 'px');
            $('#EditorTd').css('display', 'none');
        }
        else if (mode == 'edit') {
            $('#FileBrowserTd').css('display', 'none');
            $('#EditorTd').css('width', Math.floor(0.5 * window.innerWidth) + 'px').css('display', '');
            Editor.update();
        }
    },
    _log : function(msg)
    {
        console.log('Toolbar# ' + msg);
    }
};
