
var Toolbar = {
    init : function(files) {
        $("#FileNameInput").autocomplete({
            source: files,
            minLength: 0,
            delay: 100,
        }).click(function() {
            $(this).autocomplete('search', '');
        });
    }
};
