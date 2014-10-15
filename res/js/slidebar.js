(function() {
    function Debug(msg) {
        console.log(msg);
    }

    function GetPosition(elem) {
        var x = 0;
        var y = 0;
        var node = elem;
        while (node) {
            if (node.offsetLeft)
                x += node.offsetLeft;
            if (node.offsetTop)
                y += node.offsetTop;
            node = node.offsetParent;
        }
        return {x:x, y:y};
    }

    function Hide(elem) {
        elem.style.position = 'absolute';
        elem.style.left ='-1000px';
    }

    window.InitSlideBar = function(aBarId, aTriggerId)
    {
        //隐藏节点
        var barElem = document.getElementById(aBarId);
        Hide(barElem);

        //触发节点显示
        var triggerElem = document.getElementById(aTriggerId);
        triggerElem.addEventListener('mouseover',
            function() {
                var pos = GetPosition(triggerElem);
                Debug('Slidebar trigger mousemover pos=' + pos);
                barElem.style.left = pos.x + 'px';
                barElem.style.top = (pos.y - barElem.clientHeight) + 'px';
            });

        //重新隐藏
        barElem.addEventListener('mouseleave',
            function() {
                Hide(barElem);
            });

    }
})()
