
var Toolbar = {
    files : [],
    init : function(files) {
        //获取控件
        this.fileNameInput = $("#FileNameInput");

        //获取文件列表
        this.files = files;
        this.files.sort(function (a, b) {
            return a.toLowerCase().localeCompare(b.toLowerCase());
         });

        //输入框自动完成
        this.fileNameInput.autocomplete({
            source: files,
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

        //根据url hash打开文件
        if (window.location.hash) {
            var fileName = unescape(window.location.hash.substr(1));
            this.fileNameInput.val(fileName);
            Editor.editFile(fileName);
        }

    },
    addFile : function(name)
    {
        this.files.push(name);
        this.init(this.files);
    },
};
