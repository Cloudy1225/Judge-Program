// 引入FileSaver.js文件
//document.write("<script  src='FileSaver.js'></script>");
// 为使文件结构更好看，我将src文件夹下的FileSaver.js删除，文件中代码直接复制于下方，其封装了文件保存功能
(function (global, factory) {
    if (typeof define === "function" && define.amd) {
        define([], factory);
    } else if (typeof exports !== "undefined") {
        factory();
    } else {
        var mod = {
            exports: {}
        };
        factory();
        global.FileSaver = mod.exports;
    }
})(this, function () {
    "use strict";

    /*
    * FileSaver.js
    * A saveAs() FileSaver implementation.
    *
    * By Eli Grey, http://eligrey.com
    *
    * License : https://github.com/eligrey/FileSaver.js/blob/master/LICENSE.md (MIT)
    * source  : http://purl.eligrey.com/github/FileSaver.js
    */
    // The one and only way of getting global scope in all environments
    // https://stackoverflow.com/q/3277182/1008999
    var _global = typeof window === 'object' && window.window === window ? window : typeof self === 'object' && self.self === self ? self : typeof global === 'object' && global.global === global ? global : void 0;

    function bom(blob, opts) {
        if (typeof opts === 'undefined') opts = {
            autoBom: false
        };else if (typeof opts !== 'object') {
            console.warn('Deprecated: Expected third argument to be a object');
            opts = {
                autoBom: !opts
            };
        } // prepend BOM for UTF-8 XML and text/* types (including HTML)
        // note: your browser will automatically convert UTF-16 U+FEFF to EF BB BF

        if (opts.autoBom && /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) {
            return new Blob([String.fromCharCode(0xFEFF), blob], {
                type: blob.type
            });
        }

        return blob;
    }

    function download(url, name, opts) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.responseType = 'blob';

        xhr.onload = function () {
            saveAs(xhr.response, name, opts);
        };

        xhr.onerror = function () {
            console.error('could not download file');
        };

        xhr.send();
    }

    function corsEnabled(url) {
        var xhr = new XMLHttpRequest(); // use sync to avoid popup blocker

        xhr.open('HEAD', url, false);

        try {
            xhr.send();
        } catch (e) {}

        return xhr.status >= 200 && xhr.status <= 299;
    } // `a.click()` doesn't work for all browsers (#465)


    function click(node) {
        try {
            node.dispatchEvent(new MouseEvent('click'));
        } catch (e) {
            var evt = document.createEvent('MouseEvents');
            evt.initMouseEvent('click', true, true, window, 0, 0, 0, 80, 20, false, false, false, false, 0, null);
            node.dispatchEvent(evt);
        }
    } // Detect WebView inside a native macOS app by ruling out all browsers
    // We just need to check for 'Safari' because all other browsers (besides Firefox) include that too
    // https://www.whatismybrowser.com/guides/the-latest-user-agent/macos


    var isMacOSWebView = /Macintosh/.test(navigator.userAgent) && /AppleWebKit/.test(navigator.userAgent) && !/Safari/.test(navigator.userAgent);
    var saveAs = _global.saveAs || ( // probably in some web worker
        typeof window !== 'object' || window !== _global ? function saveAs() {}
            /* noop */
            // Use download attribute first if possible (#193 Lumia mobile) unless this is a macOS WebView
            : 'download' in HTMLAnchorElement.prototype && !isMacOSWebView ? function saveAs(blob, name, opts) {
                    var URL = _global.URL || _global.webkitURL;
                    var a = document.createElement('a');
                    name = name || blob.name || 'download';
                    a.download = name;
                    a.rel = 'noopener'; // tabnabbing
                    // TODO: detect chrome extensions & packaged apps
                    // a.target = '_blank'

                    if (typeof blob === 'string') {
                        // Support regular links
                        a.href = blob;

                        if (a.origin !== location.origin) {
                            corsEnabled(a.href) ? download(blob, name, opts) : click(a, a.target = '_blank');
                        } else {
                            click(a);
                        }
                    } else {
                        // Support blobs
                        a.href = URL.createObjectURL(blob);
                        setTimeout(function () {
                            URL.revokeObjectURL(a.href);
                        }, 4E4); // 40s

                        setTimeout(function () {
                            click(a);
                        }, 0);
                    }
                } // Use msSaveOrOpenBlob as a second approach
                : 'msSaveOrOpenBlob' in navigator ? function saveAs(blob, name, opts) {
                        name = name || blob.name || 'download';

                        if (typeof blob === 'string') {
                            if (corsEnabled(blob)) {
                                download(blob, name, opts);
                            } else {
                                var a = document.createElement('a');
                                a.href = blob;
                                a.target = '_blank';
                                setTimeout(function () {
                                    click(a);
                                });
                            }
                        } else {
                            navigator.msSaveOrOpenBlob(bom(blob, opts), name);
                        }
                    } // Fallback to using FileReader and a popup
                    : function saveAs(blob, name, opts, popup) {
                        // Open a popup immediately do go around popup blocker
                        // Mostly only available on user interaction and the fileReader is async so...
                        popup = popup || open('', '_blank');

                        if (popup) {
                            popup.document.title = popup.document.body.innerText = 'downloading...';
                        }

                        if (typeof blob === 'string') return download(blob, name, opts);
                        var force = blob.type === 'application/octet-stream';

                        var isSafari = /constructor/i.test(_global.HTMLElement) || _global.safari;

                        var isChromeIOS = /CriOS\/[\d]+/.test(navigator.userAgent);

                        if ((isChromeIOS || force && isSafari || isMacOSWebView) && typeof FileReader !== 'undefined') {
                            // Safari doesn't allow downloading of blob URLs
                            var reader = new FileReader();

                            reader.onloadend = function () {
                                var url = reader.result;
                                url = isChromeIOS ? url : url.replace(/^data:[^;]*;/, 'data:attachment/file;');
                                if (popup) popup.location.href = url;else location = url;
                                popup = null; // reverse-tabnabbing #460
                            };

                            reader.readAsDataURL(blob);
                        } else {
                            var URL = _global.URL || _global.webkitURL;
                            var url = URL.createObjectURL(blob);
                            if (popup) popup.location = url;else location.href = url;
                            popup = null; // reverse-tabnabbing #460

                            setTimeout(function () {
                                URL.revokeObjectURL(url);
                            }, 4E4); // 40s
                        }
                    });
    _global.saveAs = saveAs.saveAs = saveAs;

    if (typeof module !== 'undefined') {
        module.exports = saveAs;
    }
});



/**
 * 上传文件并在textarea中显示
 */
window.onload = function() {
    /**
     * 上传函数
     * @param fileInput DOM对象
     * @param callback 回调函数
     */
    var getFileContent = function (fileInput, callback) {
        if (fileInput.files && fileInput.files.length > 0 && fileInput.files[0].size > 0) {
            //下面这一句相当于JQuery的：var file =$("#upload").prop('files')[0];
            var file = fileInput.files[0];
            if (window.FileReader) {
                var reader = new FileReader();
                reader.onloadend = function (evt) {
                    if (evt.target.readyState === FileReader.DONE) {
                        callback(evt.target.result);
                    }
                };
                // 包含中文内容用utf-8编码
                reader.readAsText(file, 'utf-8');
            }
        }
    };

    /**
     * upload内容变化时载入内容
     */
    document.getElementById('uploadButton').onchange = function () {
        var textArea = document.getElementById('textArea');
        getFileContent(this, function (str) {
            textArea.value = str;
        });
    };
};

/**
 * 清空案例文本
 */
function clearContent(){
    var textArea = document.getElementById('textArea'); // 文本域文档元素：案件文本
    textArea.value = "";
}

/**
 * 清空标注
 */
function clearMark(){
    var tab__contentList = document.getElementsByClassName("tab__content");//长度为7
    for(var i = 0; i < tab__contentList.length; i++){
        //var checkboxes = tab__contentList[i].getElementsByClassName("checkboxItem");
        var checkboxes = tab__contentList[i].getElementsByTagName("input");
        for(var j = 0; j < checkboxes.length; j++){
            checkboxes[j].checked = false;
        }
    }
}
/**
 * 保存案件文本和标注
 */
function saveFile(){
    saveTxt();
    saveJSON();
}
// 保存案件文本.txt
function saveTxt(){
    var textArea = document.getElementById('textArea'); // 文本域文档元素：案件文本
    var textAreaContent = textArea.value; // 具体内容
    if(textAreaContent){ // 有内容
        var blob = new Blob([textAreaContent], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "案件文本.txt");
        //textArea.value="";// 清空输入框
    }else{ // 无内容
        window.alert("你尚未输入案件文本，请重新输入");
    }
}
// 保存标注.json
/*function saveJSON(){
    var textList = document.querySelectorAll(".text"); // 所有的text文档元素： 标注

    var unMarked = ""; //尚为标注的信息
    // 获取未标注的信息名称
    for(var i = 0; i < textList.length; i++){
        if(!textList[i].value){
            unMarked += (textList[i].placeholder + "，");
        }
    }

    if(unMarked){ // 有未标注的
        window.alert("你尚未标注：" + unMarked + "请标注");
    }else { // 全都标注了
        var textContents = []; // text具体内容数组
        for(var i = 0; i < textList.length; i++){
            var textJSONString = '"' + textList[i].placeholder + '":' + '"' + textList[i].value + '"'; // 每个标注的字符串
            textContents.push(textJSONString);
        }
        var textListJSONString = "{" + textContents.join(",") + "}"; // JSON字符串
        var blob = new Blob([textListJSONString], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "标注.json");
    }
}*/

//添加复选框
function addCheckbox(){

    var jieba1 = [];
    var jieba2 = [];
    var jieba3 = [];
    var jieba4 = [];

    //不涉及地点名词
    var nouns = document.createElement('div'); //创建名词div
    var title1 = document.createElement('h3');
    title1.innerText = "不涉及地点名词";
    nouns.appendChild(title1);
    for(var i = 0; i < jieba1.length; i++){
        var checkBox = document.createElement("input"); //创建复选框
        checkBox.setAttribute("type", "checkbox"); //复选框旁的文字
        var label = document.createElement("label");
        label.setAttribute("class", "checkbox-inline");
        label.appendChild(checkBox);
        var text = document.createTextNode(jieba1[i]); //复选框旁的文字
        label.appendChild(text);
        nouns.appendChild(label);
    }

    //涉及地点名词
    var verbs = document.createElement('div'); //创建名词div
    var title2 = document.createElement('h3');
    title2.innerText = "涉及地点名词";
    verbs.appendChild(title2);
    for(var i = 0; i < jieba2.length; i++){
        var checkBox = document.createElement("input"); //创建复选框
        checkBox.setAttribute("type", "checkbox"); //复选框旁的文字
        var label = document.createElement("label");
        label.setAttribute("class", "checkbox-inline");
        label.appendChild(checkBox);
        var text = document.createTextNode(jieba2[i]); //复选框旁的文字
        label.appendChild(text);
        verbs.appendChild(label);
    }

    //案由
    var adjs = document.createElement('div'); //创建名词div
    var title3 = document.createElement('h3');
    title3.innerText = "案由";
    adjs.appendChild(title3);
    for(var i = 0; i < jieba3.length; i++){
        var checkBox = document.createElement("input"); //创建复选框
        checkBox.setAttribute("type", "checkbox"); //复选框旁的文字
        var label = document.createElement("label");
        label.setAttribute("class", "checkbox-inline");
        label.appendChild(checkBox);
        var text = document.createTextNode(jieba3[i]); //复选框旁的文字
        label.appendChild(text);
        adjs.appendChild(label);
    }

    //形容词
    var courses = document.createElement('div'); //创建名词div
    var title4 = document.createElement('h3');
    title4.innerText = "形容词";
    courses.appendChild(title4);
    for(var i = 0; i < jieba4.length; i++){
        var checkBox = document.createElement("input"); //创建复选框
        checkBox.setAttribute("type", "checkbox"); //复选框旁的文字
        var label = document.createElement("label");
        label.setAttribute("class", "checkbox-inline");
        label.appendChild(checkBox);
        var text = document.createTextNode(jieba4[i]); //复选框旁的文字
        label.appendChild(text);
        courses.appendChild(label);
    }

    var tabs =document.getElementById("jiebas");//获取选项卡
    var jiebas = document.createElement("div");
    jiebas.setAttribute("class", "tab__content");
    jiebas.appendChild(nouns);
    jiebas.appendChild(verbs);
    jiebas.appendChild(adjs);
    jiebas.appendChild(courses);
    tabs.appendChild(jiebas)
}



// 保存标注.json
function saveJSON(){
    //var textList = document.querySelectorAll(".text"); // 所有的text文档元素： 标注

    var tab__contentList = document.getElementsByClassName("tab__content");//长度为7
    var markList = new Array(tab__contentList.length);
    for(var i = 0; i < tab__contentList.length; i++){
        //var checkboxes = tab__contentList[i].getElementsByClassName("checkboxItem");
        var checkboxes = tab__contentList[i].getElementsByTagName("input");
        markList[i] = "";
        for(var j = 0; j < checkboxes.length; j++){
            if(checkboxes[j].checked){
                var label = checkboxes[j].parentNode;
                if(markList[i].length != 0) {
                    markList[i] += ("、" + label.innerText);
                }else {
                    markList[i] = label.innerText;
                }
            }
        }
    }

    var nameList = ["当事人", "性别", "民族", "出生地", "文化水平", "案由", "相关法院"];
    var textContents = [];
    for (var i = 0; i < 7; i++){
        var textJSONString = '"' + nameList[i] + '":' + '"' + markList[i] + '"';
        textContents.push(textJSONString);
    }
    var textListJSONString = "{" + textContents.join(",") + "}"; // JSON字符串
    var blob = new Blob([textListJSONString], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "标注.json");

    /*var unMarked = ""; //尚为标注的信息
    // 获取未标注的信息名称
    for(var i = 0; i < textList.length; i++){
        if(!textList[i].value){
            unMarked += (textList[i].placeholder + "，");
        }
    }

    if(unMarked){ // 有未标注的
        window.alert("你尚未标注：" + unMarked + "请标注");
    }else { // 全都标注了
        var textContents = []; // text具体内容数组
        for(var i = 0; i < textList.length; i++){
            var textJSONString = '"' + textList[i].placeholder + '":' + '"' + textList[i].value + '"'; // 每个标注的字符串
            textContents.push(textJSONString);
        }
        var textListJSONString = "{" + textContents.join(",") + "}"; // JSON字符串
        var blob = new Blob([textListJSONString], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "标注.json");
    }*/
}

