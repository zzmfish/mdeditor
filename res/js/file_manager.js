
var FileManager = {
    _request: function(path, params) {
        var url = path;
        var firstParam = true;
        for (paramName in params) {
            if (firstParam)
                url += '?';
            else
                url += '&';
            url += paramName + '=' + encodeURIComponent(params[paramName]);
            firstParam = false;
        }
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
    },

    move: function(oldPath, newPath) {
        FileManager._request('/move', {from:oldPath, to:newPath});
    },

    createFolder: function(path) {
        FileManager._request('/mkdir', {name:path});
    }
};