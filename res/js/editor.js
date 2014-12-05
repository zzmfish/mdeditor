
var Editor = {
    init : function()
    {
        //初始化编辑器
        var editor = ace.edit("Editor");
        editor.setTheme("ace/theme/kuroir");
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


};
