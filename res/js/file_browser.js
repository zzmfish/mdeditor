
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
        $("#FileBrowser").jstree(data)
    },

    _buildTreeData : function(files) {
        FileBrowser._log("_buildTreeData")
        var rootNode = {}
        for (var fileIndex = 0; fileIndex < files.length; fileIndex ++) {
            var file = files[fileIndex];
            var pathParts = file.replace('\\', '/').split('/')
            console.log(pathParts)
            var dirNode = rootNode;
            for (var dirIndex = 0; dirIndex < pathParts.length - 1; dirIndex ++) {
                var dirName = pathParts[dirIndex];
                if (dirNode[dirName] == undefined)
                    dirNode[dirName] = {"text": dirName, "children": []}
                dirNode = dirNode[dirName]
            }
        }
        console.log(rootNode);
        return rootNode;
    },

    _buildShowData : function(data) {
        FileBrowser._log("_buildShowData")
        var showData = []
        if (Array.isArray(data)) {
        } else {
            for (var dirName in data) {
                console.log(dirName)
                var nodeData = {
                    "text": dirName,
                    "children": [],
                }
                showData.push(nodeData);
            }
        }
        return showData;
    },

    _log : function(msg) {
        console.log('FileBrowser# ' + msg)
    }
};