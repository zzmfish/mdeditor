
var FileBrowser = {

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
                            var tree = FileBrowser._getTree(),
                                obj = tree.get_node(data.reference);
                            tree.create_node(obj, {}, "last", function (new_node) {
                                setTimeout(function () { tree.edit(new_node); },0);
                            });
                        }
                    },
                    create_file: {
                        label: "笔记",
                        action: function (data) {
                            var tree = FileBrowser._getTree(),
                                obj = tree.get_node(data.reference);
                            tree.create_node(obj, {"icon" : "jstree-file"}, "last", function (new_node) {
                                setTimeout(function () { tree.edit(new_node); },0);
                            });
                        }
                    },
                }
            },
            remove: {
                label: "删除",
                action: function (data) {
                    var tree = FileBrowser._getTree();
                    var obj = tree.get_node(data.reference);
                    if(tree.is_selected(obj)) {
                        tree.delete_node(tree.get_selected());
                    }
                    else {
                        tree.delete_node(obj);
                    }
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
                .on("mousedown", function (e) {
                    var node = e.target;
                    if (! node.classList.contains('jstree-anchor'))
                        return;
                    var tree = FileBrowser._getTree();
                    if (tree.is_selected(node)) {
                        setTimeout(function () { tree.edit(node); },0);
                    }
                    else {
                        var path = tree.get_path(node, '/');
                        var isLeaf = tree.is_leaf(node);
                        console.log('FileBrowser click: path=' + path + ', is_leaf=' + isLeaf);
                        if (isLeaf) {
                            FileBrowser.onOpen(path);
                        }
                    }
                })
                .on("create_node.jstree", function(e, data) {
                    var tree = FileBrowser._getTree();
                    var path = tree.get_path(data.node, '/');
                    if (data.node.icon == "jstree-file")
                        FileBrowser.onCreateFile(path);
                    else
                        FileBrowser.onCreateFolder(path);
                })
                .on("rename_node.jstree", function(e, data) {
                    var newPath = FileBrowser._getPath(data.node);
                    var oldName = data.old;
                    var oldPath = "";
                    if (newPath.indexOf('/') >= 0)
                        oldPath = newPath.replace(/\/[^\/]*$/, '/' + oldName);
                    else
                        oldPath = oldName;
                    FileBrowser.onMove(oldPath, newPath);
                })
                .on("delete_node.jstree", function(e, data) {
                    var tree = FileBrowser._getTree();
                    var path = tree.get_path(data.node, '/');
                    FileBrowser.onDelete(path);
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

    onOpen : function(filePath) {},

    onMove : function(oldName, newName) {},

    onCreateFolder : function(path) {},

    onCreateFile : function(path) {},

    onDelete : function(path) {},

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
