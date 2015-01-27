
var Toolbar = {
    files : [],
    init : function(files) {
        this.files = files;
        this.files.sort(function (a, b) {
            return a.toLowerCase().localeCompare(b.toLowerCase());
         });;
        $("#FileNameInput").autocomplete({
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
        });
    },
    addFile : function(name)
    {
        this.files.push(name);
        this.init(this.files);
    },
};
