

/////////////////////////////////////////字符串操作///////////////////////////
function GetFileNameByPath(s) {
    if (s.indexOf("\\") > -1)
        return s.match(/\\([^\\^.]+)\.[^\\]*$/)[1];
    else
        return s;

}
//验证输入框输入的值是否不正整数,否置为1
function isint(ob) {
    var Reg = /^[1-9]\d*$/;
    return Reg.test($(ob).val());
}
///////////////////////////////////////////////////////////////////////////////////
// String Helper
///////////////////////////////////////////////////////////////////////////////////
String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,
        function (m, i) {
            return args[i];
        });
}

String.format = function () {
    if (arguments.length == 0)
        return null;

    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}

/////////////////////////
///去前后空格
////////////////////////
String.prototype.trim = function () {
    return this.replace(/(^\s*)|(\s*$)/g, "");
}
String.prototype.ltrim = function () {
    return this.replace(/(^\s*)/g, "");
}
String.prototype.rtrim = function () {
    return this.replace(/(\s*$)/g, "");
}

//定义一个字符stringbuilder类
function StringBuilder() {
    this.arrStr = new Array();
}
StringBuilder.prototype.Append = function (strVelue) {
    this.arrStr.push(strVelue);
}

StringBuilder.prototype.toString = function () {
    return this.arrStr.join("");

}
function getFileExt(str) {
    var d = /\.[^\.]+$/.exec(str);
    return d.toString().toLowerCase() ;
}

//获取url?号后的参数
function GetUrlParams(ParamName) {
    var URLParams = new Object();
    var aParams = document.location.search.substr(1).split('&');
    for (i = 0; i < aParams.length; i++) {
        var aParam = aParams[i].split('=');
        URLParams[aParam[0]] = aParam[1];
    }

    var sValue = URLParams[ParamName];
    if (sValue == undefined)
        return "";
    return sValue;
}

function cut_string(strString, nLength) {
    var nTheLength = 0;
    for (var nIndex = 0; nIndex < strString.length; nIndex++) {
        if (strString.charCodeAt(nIndex) > 255)
            nTheLength += 2;
        else
            nTheLength += 1;
        if (nTheLength >= nLength)
            break;
    }
    var strResult = strString.substr(0, nIndex);
    if (strResult.length < strString.length)
        strResult = strResult + "...";
    return strResult;
}
function cut_str_mid(strString, iLength) {
    if (strString.length > iLength) {
        var iLength2 = parseInt(iLength / 2);
        var strtemp1 = strString.substr(0, iLength2);
        var strtemp2 = strString.substr(strString.length - iLength2);
        strString = "";
        strString = strtemp1 + "  ...  " + strtemp2;
    }
    return strString;
}
//从url中获取文件类型
function get_type_of_url(sUrl) {
    var strType = "";
    if (sUrl != "") {
        var iLastIndex = sUrl.lastIndexOf(".") + 1;
        strType = sUrl.substring(iLastIndex, sUrl.length);

    }
    if (strType.length > 5) return "";
    return strType;
}
//复制文本
function CopyObText(thisobj) {
    var rng = document.body.createTextRange();
    rng.moveToElementText(thisobj);
    rng.scrollIntoView();
    rng.select();
    clipboardData.setData('text', thisobj.innerText);
    alert("复制成功!!");
}
function JsonToObj(sJson) {

    return eval("({" + sJson + "})");
}

//////////////////////////////////数组操作///////////////////////

//为数组添加一个删除指定索引项  
Array.prototype.contains = function (element) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == element) {
            return true;
        }
    }
    return false;
} 
Array.prototype.removecount = 0;
Array.prototype.removedAt = function (index) {
    if (isNaN(index) || index < 0) {
        return;
    }
    if (index < this.length) {
        this.splice(index, 1);
        this.removecount++;
    }

}
//为数组添加一个新办法:删除重复数组项。
Array.prototype.unique = function () {
    var tempArray = this.slice(0); //复制数组到临时数组
    for (var i = 0; i < tempArray.length; i++) {
        for (var j = i + 1; j < tempArray.length; ) {
            if (tempArray[j].toString() == tempArray[i].toString())
            //后面的元素若和待比较的相同，则删除并计数；
            //删除后，后面的元素会自动提前，所以指针j不移动
            {
                tempArray.splice(j, 1);
            }
            else {
                j++;
            }
            //不同，则指针移动
        }
    }
    return tempArray;
}


//从指定值获取数组索引,如有重复值，只取第一个索引
Array.prototype.GetIndex = function (obj) {
    var tempArray = this.slice(0); //复制数组到临时数组
    var iIndex = 0;
    for (var i = 0; i < tempArray.length; i++) {
        if (tempArray[i]==obj) {
            iIndex = i;
            break;
        }
    }

    return iIndex;
}


//GET办法运行异步http请求
function run_ajax_async(url, postdata, backfun) 
{
     
    $.ajax({
        type: "get",
        url: url,
        data: postdata,
        beforeSend: onAjaxBeforeSend,
        dataType: "html",
        success: function (msg) {
            if (backfun != null) backfun(msg);

        },
        async: true
    });
}
//GET/post办法运行异步http请求
function run_ajax_async_type(url, postdata, backfun, stype) {
    
    $.ajax({
        type: stype,
        url: url,
        data: postdata,
        beforeSend: onAjaxBeforeSend,
        dataType: "html",
        success: function (msg) {
            if (backfun != null) backfun(msg);

        },
        async: true
    });
}
//异步json
function run_ajax_async_json(url, postobj, backfun) {
    
    var obpram = postobj;
    if (postobj == null || postobj == "")
        obpram = {};      

    $.ajax({
        url: url,
        data: JSON.stringify(obpram),
        type: "POST",
        contentType: "application/json; charset=utf-8",//application/x-www-form-urlencoded, application/json; charset=utf-8
        dataType: "json",
        // beforeSend: onAjaxBeforeSend,
        success: function (result) {

            if (backfun != null) backfun(result);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $.log("调用ajax发生错误:" + thrownError + " 调用地址:" + url);
            //alert("调用ajax发生错误:" + thrownError);
        }

    });
}

function get_ajax(url,backfun) {
     
    $.ajax({
        url: url, 
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        beforeSend: onAjaxBeforeSend,
        success: function (result) {
            if (backfun != null) backfun(result);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $.log("调用ajax发生错误:" + thrownError + " 调用地址:" + url);
            //alert("调用ajax发生错误:" + thrownError);
        }

    });
}
//同步json
function run_ajax_unasync_json(url, postobj) {

    var vlMsg;
    var obpram = postobj;
    if (postobj == null || postobj == "")
        obpram = {};
    
    $.ajax({
        url: url,
        async: false,
        data: JSON.stringify(obpram),
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        beforeSend: onAjaxBeforeSend,
        success: function (result) {
            vlMsg = result;
        },
        error: function (xhr, ajaxOptions, thrownError) {

            $.log("调用ajax发生错误:" + thrownError);
            //alert("调用ajax发生错误:" + thrownError);
        }

    });
    return vlMsg;
}

//运行同步http请求
function run_ajax_unasync(url) {
    var html = $.ajax({
        url: url,
        beforeSend: onAjaxBeforeSend,
        async: false
    }).responseText;

    return html;
}
//GET办法运行异步http请求 javascript
function run_ajax_async_js(url, postdata, backfun) {

    $.ajax({
        type: "get",
        url: url,
        data: postdata,
        dataType: "script",
        beforeSend: onAjaxBeforeSend,
        success: function (msg) {
            if (backfun != null) backfun(msg);

        },
        async: true
    })
}

//可以动态载入js的json对象
function get_json(sPath, fun) {
    $.getJSON(sPath,
                fun
        );
}

//批量操作----------------------------------------
//获取某个元素下的所有check值，用逗号分开
function GetCheckValues(obid) {
    var aValues = [];
    var obHtml = $("#" + obid);
    obHtml.find("input[type=checkbox]").each(
		function (i) {
		    if (this.checked) {
		        aValues.push($(this).val());
		    }
		}
		);

    return aValues.join(",");
}


//反向选取
function on_check(obchk) {
    var ob = $(obchk).parent().parent().parent().parent();
    $(ob).find("input[type=checkbox]").each(
        function (i) {
            this.checked = obchk.checked;
        }
    );
}
function get_checkboxval(seletetor) {
    var aValues = [];
    var obHtml = $(seletetor);
    obHtml.find("input[type=checkbox]").each(
        function (i) {
            if (this.checked) {
                aValues.push($(this).val());
            }
        }
    );
    return aValues.join(",");
}


//获取选择的radio值
function get_checkedradio_value(radios) {
    for (var i = 0; i <= radios.length; i++) {
        if (radios[i].checked) return radios[i].value;
    }
    return null;
}
function set_radio_checked(obradio, v) {
    var radios = $(obradio);
    for (var i = 0; i < radios.length; i++) {
        
        if (radios[i].value == v) {
            radios[i].checked = true;
        }
    }
    return null;
}

//获取下拉列表项
function get_selected_value(ob) {

    return ob.options[ob.selectedIndex].value;
}
function get_selected_text(ob) {

    return ob.options[ob.selectedIndex].text;
}
function set_selected_value(ob, value) {
    $(ob).attr("value", value);

}
//pos = -1 为添加,pos=0为插入
function add_selecte_option(obID, svalue, stext, pos) {

    var strName = stext;
    var strValue = svalue;
    $("#" + obID).append("<option pram=\"" + pos + "\" value=\"" + strValue + "\">" + strName + "</option>");
}
// 删除选项,type 为采用不同的方法
function delete_selecte_option(obID, keepindex) {

    $("#" + obID).find("option").each(
		function (i) {

		    if (i != keepindex)
		        $(this).remove();

		}
		);
}
//删除所选项
function delete_sel_item(obID) {
    $("#" + obID).find("option:selected").remove();
}

function Refesh() {
    var url = location.href;
    if (url.lastIndexOf("#") > 0) {
        url = url.substring(0, url.length - 1);
    }
    
    document.location.href = url;
}
function RefeshParent() {
    parent.document.location.href = parent.document.location.href;
}

function gotourl(url) {
    document.location.href = url;
}

function unBlock() {
    In.ready('blockui', function () {
        $.unblockUI();
    });
}

/**
 * 加载弹出框
 * @param msg
 * @param time
 */
function blockTips(msg, time) {
    var iTime = 0;
    if (arguments.length == 2) {
        iTime = time;
    }

    var msgHtml = '<div class="blockTips">' + msg + '</div>';
    iTime = iTime * 1000;
    In.ready('blockui', function () {
        //执行代码
        $.blockUI({
            message: msgHtml,
            timeout: iTime, //unblock after 2 seconds
            overlayCSS: {
                backgroundColor: '#1b2024',
                opacity: 0.8,
                cursor: 'wait'
            },
            css: {
                border: 0,
                color: '#fff',
                padding: 0,
                backgroundColor: 'transparent'
            }
        });
    });

}

//常用插件开发

; (function ($, window, document, undefined) {
    $.extend({
        log: function (message) {
            var now = new Date(),
                y = now.getFullYear(),
                m = now.getMonth() + 1,
                d = now.getDate(),
                h = now.getHours(),
                min = now.getMinutes(),
                s = now.getSeconds(),
                time = y + '/' + m + '/' + d + ' ' + h + ':' + min + ':' + s;
            console.log("日志输出: " + message + "       时间:" + time);
        }

    });
    $.extend({
        logobj: function (obj) {
            $.log(JSON.stringify(obj));
        }

    });

    $.fn.LoadNoRefresh = function (options) {
        var defaults = {
            'itembox': '#panelzxtab1',//listview 盒子
            'nextpagebox': '.pagination',//分页盒子
            'nextpage': '.nextpage',//下页带href的元素
            'loadingtxt': '正在加载中...'//点击加载提示
        };
        var settings = $.extend({}, defaults, options);//将一个空对象做为第一个参数,保护默认设置
        $(settings.nextpagebox).hide();
        var nextpage = $(settings.nextpage).attr("href");

        var btnoldtxt = $(this).html();
        var _this = this;
        this.click(function () {
            $(this).html(settings.loadingtxt);
            $('<div/>').appendTo(settings.itembox).load(nextpage + " " + settings.itembox, function (responseText) {

                var obj = $(responseText).find(settings.nextpage);

                nextpage = obj.attr("href");
                _this.html(btnoldtxt);

                if (!nextpage) {
                    _this.hide();
                }


            });
        });
    }
})(jQuery, window, document);

    (function() {
        'use strict';
        window.addEventListener('load', function() {
            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            var forms = document.getElementsByClassName('needs-validation');

            // Loop over them and prevent submission
            var validation = Array.prototype.filter.call(forms, function(form) {
                form.addEventListener('submit', function(event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);
    })();

// inc--start
~function () { var __head = document.head || document.getElementsByTagName("head")[0]; var __waterfall = {}; var __loaded = {}; var __loading = {}; var __configure = { autoload: false, core: "", serial: false }; var __in; var __load = function (url, type, charset, callback) { if (__loading[url]) { if (callback) { setTimeout(function () { __load(url, type, charset, callback) }, 1); return } return } if (__loaded[url]) { if (callback) { callback(); return } return } __loading[url] = true; var pureurl = url.split("?")[0]; var n, t = type || pureurl.toLowerCase().substring(pureurl.lastIndexOf(".") + 1); if (t === "js") { n = document.createElement("script"); n.type = "text/javascript"; n.src = url; n.async = "true"; if (charset) { n.charset = charset } } else { if (t === "css") { n = document.createElement("link"); n.type = "text/css"; n.rel = "stylesheet"; n.href = url; __loaded[url] = true; __loading[url] = false; __head.appendChild(n); if (callback) { callback() } return } } n.onload = n.onreadystatechange = function () { if (!this.readyState || this.readyState === "loaded" || this.readyState === "complete") { __loading[url] = false; __loaded[url] = true; if (callback) { callback() } n.onload = n.onreadystatechange = null } }; n.onerror = function () { __loading[url] = false; if (callback) { callback() } n.onerror = null }; __head.appendChild(n) }; var __analyze = function (array) { var riverflow = []; for (var i = array.length - 1; i >= 0; i--) { var current = array[i]; if (typeof (current) === "string") { if (!__waterfall[current]) {  continue } riverflow.push(current); var relylist = __waterfall[current].rely; if (relylist) { riverflow = riverflow.concat(__analyze(relylist)) } } else { if (typeof (current) === "function") { riverflow.push(current) } } } return riverflow }; var __stackline = function (blahlist) { var o = this; this.stackline = blahlist; this.current = this.stackline[0]; this.bag = { returns: [], complete: false }; this.start = function () { if (typeof (o.current) != "function" && __waterfall[o.current]) { __load(__waterfall[o.current].path, __waterfall[o.current].type, __waterfall[o.current].charset, o.next) } else { o.bag.returns.push(o.current()); o.next() } }; this.next = function () { if (o.stackline.length == 1 || o.stackline.length < 1) { o.bag.complete = true; if (o.bag.oncomplete) { o.bag.oncomplete(o.bag.returns) } return } o.stackline.shift(); o.current = o.stackline[0]; o.start() } }; var __parallel = function (blahlist, callback) { var length = blahlist.length; var hook = function () { if (! --length && callback) { callback() } }; if (length == 0) { callback && callback(); return } for (var i = 0; i < blahlist.length; i++) { var current = __waterfall[blahlist[i]]; if (typeof (blahlist[i]) == "function") { blahlist[i](); hook(); continue } if (current.rely && current.rely.length != 0) { __parallel(current.rely, (function (current) { return function () { __load(current.path, current.type, current.charset, hook) } })(current)) } else { __load(current.path, current.type, current.charset, hook) } } }; var __add = function (name, config) { if (!name || !config || !config.path) { return } __waterfall[name] = config }; var __adds = function (config) { if (!config.modules) { return } for (var module in config.modules) { var module_config = config.modules[module]; if (!config.modules.hasOwnProperty(module)) { continue } if (config.type && !module_config.type) { module_config.type = config.type } if (config.charset && !module_config.charset) { module_config.charset = config.charset } __add.call(this, module, module_config) } }; var __config = function (name, conf) { __configure[name] = conf }; var __css = function (csstext) { var css = document.getElementById("in-inline-css"); if (!css) { css = document.createElement("style"); css.type = "text/css"; css.id = "in-inline-css"; __head.appendChild(css) } if (css.styleSheet) { css.styleSheet.cssText = css.styleSheet.cssText + csstext } else { css.appendChild(document.createTextNode(csstext)) } }; var __later = function () { var args = [].slice.call(arguments); var timeout = args.shift(); window.setTimeout(function () { __in.apply(this, args) }, timeout) }; var __ready = function () { var args = arguments; __contentLoaded(window, function () { __in.apply(this, args) }) }; var __in = function () { var args = [].slice.call(arguments); if (__configure.serial) { if (__configure.core && !__loaded[__configure.core]) { args = ["__core"].concat(args) } var blahlist = __analyze(args).reverse(); var stack = new __stackline(blahlist); stack.start(); return stack.bag } if (typeof (args[args.length - 1]) === "function") { var callback = args.pop() } if (__configure.core && !__loaded[__configure.core]) { __parallel(["__core"], function () { __parallel(args, callback) }) } else { __parallel(args, callback) } }; var __contentLoaded = function (win, fn) { var done = false, top = true, doc = win.document, root = doc.documentElement, add = doc.addEventListener ? "addEventListener" : "attachEvent", rem = doc.addEventListener ? "removeEventListener" : "detachEvent", pre = doc.addEventListener ? "" : "on", init = function (e) { if (e.type == "readystatechange" && doc.readyState != "complete") { return } (e.type == "load" ? win : doc)[rem](pre + e.type, init, false); if (!done && (done = true)) { fn.call(win, e.type || e) } }, poll = function () { try { root.doScroll("left") } catch (e) { setTimeout(poll, 50); return } init("poll") }; if (doc.readyState == "complete") { fn.call(win, "lazy") } else { if (doc.createEventObject && root.doScroll) { try { top = !win.frameElement } catch (e) { } if (top) { poll() } } doc[add](pre + "DOMContentLoaded", init, false); doc[add](pre + "readystatechange", init, false); win[add](pre + "load", init, false) } }; void function () { var myself = (function () { var scripts = document.getElementsByTagName("script"); return scripts[scripts.length - 1] })(); var autoload = myself.getAttribute("autoload"); var core = myself.getAttribute("core"); if (core) { __configure.autoload = eval(autoload); __configure.core = core; __add("__core", { path: __configure.core }) } if (__configure.autoload && __configure.core) { __in() } } (); __in.add = __add; __in.adds = __adds; __in.config = __config; __in.css = __css; __in.later = __later; __in.load = __load; __in.ready = __ready; __in.use = __in; this.In = __in } ();

In.add('jqcookie', { path: '/js/plugins/jquery.cookie.js', type: 'js', charset: 'utf-8' });
In.add('blockui', { path: '/js/plugins/blockui.min.js', type: 'js', charset: 'utf-8' });




