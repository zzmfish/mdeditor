(function (){
    var blockScrollEvent = false;

    window.onscroll = function() {
        if (blockScrollEvent) return;
        blockScrollEvent = true; 
        setTimeout(function() {
                var maxY = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                console.log("scrollY=" + window.scrollY + ", scrollMaxY=" + maxY);

                //通过http请求告诉服务器滚动位置
                var req_data = 'scrollY=' + window.scrollY + '&scrollMaxY=' + maxY;
                var req = new XMLHttpRequest();
                req.open('POST', '/Scroll', true);
                req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                req.setRequestHeader("Content-length", req_data.length);
                req.setRequestHeader("Connection", "close");
                req.send(req_data);

                blockScrollEvent = false;
            }, 1000);
    };
})();
