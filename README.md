mdeditor
========

在浏览器中运行的markdown编辑器，分为python后端和html/js前端，真正跨平台。
可以编辑时实时预览、或编译成静态html，最终显示效果是一样的。

## 特性
* 编辑时即时预览
* 编译成静态html，和预览一样的效果
* 跨平台：Linux/Windows/MacOS
* 程序代码语法高亮
* markdown语法高亮


## 安装和配置
### 依赖关系
* 需安装python的**Pygments**库，否则没有代码语法高亮

### 下载代码
```
git clone https://github.com/zzmfish/mdeditor.git
cd mdeditor
git submodule init
git submodule update
```

### 配置
编辑config.py，配置这几项：  

* **md_dir**: markdown源文件存储位置
* **html_dir**: markdown编译成静态html的存储位置
* **port**：端口

## 使用方法
### 编辑markdown文件
* 启动程序
```
python main.py
```
* 打开浏览器，输入`http://127.0.0.1:8889`

### 编译html
```
make
```
每个markdown文件编译成一个html文件，另外生成一个index.html。