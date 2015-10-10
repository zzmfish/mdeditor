
var FileBrowser = {
    customMenu : function(node) {
        // The default set of all items
        var items = {
            renameItem: { // The "rename" menu item
                label: "Rename",
                action: function () {
                    alert('Rename');
                }
            },
            deleteItem: { // The "delete" menu item
                label: "Delete",
                action: function () {
                    alert('Delete');
                }
            }
        };

        if ($(node).hasClass("folder")) {
            // Delete the "delete" menu item
            delete items.deleteItem;
        }

        return items;
    },

    update : function(files) {
        FileBrowser._log("update")
        FileBrowser._getTreeData(function(treeData) {
            var showData = FileBrowser._buildShowData(treeData);
            var data = {
                core: {
                    data: showData,
                },
                plugins : [ "search" , "contextmenu"],
                contextmenu: {
                    items: FileBrowser.customMenu
                },
            };
            $("#FileBrowser").jstree(data).on("changed.jstree", function (e, data) {
                if(data.selected.length) {
                    var elemId = data.selected[0];
                    var elemNode = document.getElementById(elemId);
                    console.log('select ' + elemNode);
                    if (elemNode.className.indexOf('jstree-leaf') >= 0) {
                        FileBrowser._openFile(elemNode);
                    }
                }
            });
        });
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

    _getTreeData : function(callback) {
        var req = new XMLHttpRequest();
        req.onreadystatechange = function() {
            if (req.readyState == 4) { //loaded
                if (req.status == 200) {
                    console.log(req.responseText);
                    callback(eval('(' + req.responseText + ')'));
                }
            }
        }
        req.open('GET', '/list', true);
        req.send();
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
    },
    search : function(text) {
        $('#FileBrowser').jstree(true).search(text);
    }
};
