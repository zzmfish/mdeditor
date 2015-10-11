
var FileBrowser = {

    _openedPath : null,

    customMenu : function(node) {
        // The default set of all items
        var items = {
            create: {
                label: "创建",
                action: false,
                submenu: {
                    create_folder: {
                        label: "目录",
                        action: function (data) {
                            var inst = $.jstree.reference(data.reference),
                                obj = inst.get_node(data.reference);
                            inst.create_node(obj, {}, "last", function (new_node) {
                                setTimeout(function () { inst.edit(new_node); },0);
                            });
                        }
                    },
                    create_file: {
                        label: "笔记",
                        action: function (data) {
                            alert('create file');
                        }
                    },
                }
            },
            remove: {
                label: "删除",
                action: function () {
                    alert('remove');
                }
            },
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
                    check_callback: true,
                },
                plugins : [ "search" , "contextmenu"],
                contextmenu: {
                    items: FileBrowser.customMenu
                },
            };
            FileBrowser._getTree(data)
                .on("click.jstree", function (e, data) {
                    var node = e.target;
                    var tree = FileBrowser._getTree();
                    var path = tree.get_path(node, '/');
                    var isLeaf = tree.is_leaf(node);
                    console.log('FileBrowser click: path=' + path + ', is_leaf=' + isLeaf);
                    if (isLeaf) {
                        if (path == FileBrowser._openedPath) {
                            tree.edit(node);
                        }
                        else {
                            FileBrowser.onOpen(path);
                            FileBrowser._openedPath = path;
                        }
                    }
                })
                .on("create_node.jstree", function(e, data) {
                    alert('create_node event');
                })
                .on("rename_node.jstree", function(e, data) {
                    alert('rename_node event');
                })
        });
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
    },

    _getTree: function(data) {
        return $('#FileBrowser').jstree(data || true);
    },

    _getPath: function(node) {
        return FileBrowser._getTree(true).get_path(node, '/');
    },
};
