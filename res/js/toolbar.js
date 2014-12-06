
var Toolbar = {
    init : function(files) {
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
                EditFile($(this).val());
            }
        });
    }
};
