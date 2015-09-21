
var FileBrowser = {
    update : function(files) {
        FileBrowser._log("update")
        var treeData = FileBrowser._buildTreeData(files);
        var showData = FileBrowser._buildShowData(treeData);
        var data = {
            "core": {
                "data": showData,
            }}
        console.log(data)
        $("#FileBrowser").jstree(data).on("changed.jstree", function (e, data) {
            if(data.selected.length) {
                var elemId = data.selected[0];
                var elemNode = document.getElementById(elemId);
                console.log('select ' + elemNode);
                if (elemNode.className.indexOf('jstree-leaf') >= 0) {
                    FileBrowser._openFile(elemNode);
                }
            }
        })
    },

    _openFile : function(fileNode) {
        FileBrowser._log('_openFile: ' + fileNode);
        var filePath = "";
        while (true) {
            if (fileNode.tagName == 'LI') {
                for (var childIndex = 0; childIndex < fileNode.childNodes.length; childIndex ++) {
                    var childNode = fileNode.childNodes[childIndex];
                    if (childNode.tagName == 'A') {
                        if (filePath.length > 0)
                            filePath = "/" + filePath
                        filePath = childNode.textContent + filePath;
                    }
                }
            } else if (fileNode.tagName == 'UL') {
            }
            else
                break;
            fileNode = fileNode.parentNode;
        }
        FileBrowser._log('onOpen:' + filePath)
        FileBrowser.onOpen(filePath);
    },

    _buildTreeData : function(files) {
        FileBrowser._log("_buildTreeData")
        var rootNode = {}
        for (var fileIndex = 0; fileIndex < files.length; fileIndex ++) {
            var file = files[fileIndex];
            var pathParts = file.replace(/\\/g, '/').split('/')
            console.log(pathParts)
            var dirNode = rootNode;
            for (var dirIndex = 0; dirIndex < pathParts.length - 1; dirIndex ++) {
                var dirName = pathParts[dirIndex];
                if (dirNode[dirName] == undefined)
                    dirNode[dirName] = {}
                dirNode = dirNode[dirName]
            }
            dirNode[pathParts[pathParts.length - 1]] = undefined;
        }
        console.log(rootNode);
        return rootNode;
    },

    _buildShowData : function(data) {
        FileBrowser._log("_buildShowData")
        console.log(data)
        var showData = []
        for (var dirName in data) {
            var dirData = data[dirName];
            var nodeData = undefined;
            if (dirData == undefined) {
                nodeData =  {
                    "text" : dirName,
                    "icon" : "jstree-file"
                };
            }
            else {
                nodeData = {
                    "text": dirName,
                    "children": FileBrowser._buildShowData(dirData),
                };
            }
            if (nodeData != undefined)
                showData.push(nodeData);
        }
        return showData;
    },

    _log : function(msg) {
        console.log('FileBrowser# ' + msg)
    },

    onOpen : function(filePath) {
    }
};