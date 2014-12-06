
var Toolbar = {
    init : function(files) {
        $("#FileNameInput").autocomplete({
            source: files,
            minLength: 0,
        }).click(function() {
            $(this).autocomplete('search', '');
        });
    }
};
