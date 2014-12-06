
var Toolbar = {
    files : [],
    init : function(files) {
        this.files = files;
        $("#FileNameInput").autocomplete({
            source: files,
            minLength: 0,
            delay: 100,
            select: function(e, ui) {
                EditFile(ui.item.value);
            }
        }).click(function() {
            $(this).autocomplete('search', '');
        }).keydown(function(e){
            var key = e.which;
            if (key == 13) {
                var value = $(this).val();
                if (Toolbar.files.indexOf(value) == -1) {
                    Toolbar.addFile(value);
                }
                EditFile(value);
            }
        });
    },
    addFile : function(name)
    {
        this.files.push(name);
        this.files.sort();
        this.init(this.files);
    },
};
