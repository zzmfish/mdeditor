
var FileManager = {
    move: function(oldPath, newPath)
    {
        var url = '/move?from=' + encodeURIComponent(oldPath) + '&to=' + encodeURIComponent(newPath);
        var req = new XMLHttpRequest();
        req.onreadystatechange = function() {
            if (req.readyState == 4) { //loaded
                if (req.status != 200) {
                    alert('move error');
                    console.log(req.responseText); //应答内容
                }
            }
        }
        req.open("GET", url, true);
        req.send();
    }
};