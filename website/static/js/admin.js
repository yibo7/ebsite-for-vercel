//Custom-Tags
function CustomTags() {
    //tags列表的上一级元素名称
    this.ParentObjName = "";

    this.SubObj = "";
    this.CurrentClassName = "";
    this.ClassName = "";
    this.Effects = "show"; //显示效果 show,fadein,slidedown,slideupdown,upindown
    this.fun = null;
    this.BoxList = [];
    this.TagsList = null;
    if (typeof CustomTags._initialized == "undefined") {
        CustomTags.prototype.InitOnclickInTags = function () {

            var tags = this.GetTags();
            var _objThis = $.data(document.body, "ct", this);
            if (tags != null && tags.length > 0)
            {
                for (var i = 0; i < tags.length; i++) {

                    $(tags[i]).click(function () {
                        var isallow = true;

                        if (_objThis.fun != null && _objThis.fun != "undefined") {
                            isallow = _objThis.fun(this);
                        }
                        if (isallow == undefined && isallow == null) {
                            isallow = true;
                        }
                        if (isallow) {
                            _objThis.OnclickTags(this);
                        }

                    });

                    if ($(tags[i]).attr("name") != undefined && $(tags[i]).attr("name") != null) {

                        this.BoxList.push($(tags[i]).attr("name"));
                    }

                }
            }


        }
        CustomTags.prototype.OnclickTags = function (obj) {

            var Url = $(obj).attr("u");

            if (Url == undefined) {  //tag只在当前页面使用

                this.InitCurrentClass(obj);
                var tags = this.GetTags();

                if (this.BoxList.length > 0) {
                    if (this.Effects == 'upindown') {
                        for (var i = 0; i < tags.length; i++) {

                            if (this.BoxList[i] != null) {
                                $("#" + this.BoxList[i]).slideDown();
                            }
                        }
                    }

                    for (var i = 0; i < tags.length; i++) {

                        if (this.BoxList[i] != null) {
                            if (this.Effects == 'slideupdown' || this.Effects == 'upindown')
                            { $("#" + this.BoxList[i]).slideUp(); }
                            else { $("#" + this.BoxList[i]).hide(); }

                        }
                    }
                    if (this.Effects == '' || this.Effects == 'show') {
                        $("#" + $(obj).attr("name")).show();
                    }
                    else if (this.Effects == 'fadein') {
                        $("#" + $(obj).attr("name")).fadeIn();
                    }
                    else if (this.Effects == 'slidedown' || this.Effects == 'slideupdown' || this.Effects == 'upindown') {
                        $("#" + $(obj).attr("name")).slideDown();
                    }


                }

            }
            else { //tag跨页面使用

                location.href = Url + "&tagname=" + $(obj).attr("name");

            }


        }
        CustomTags.prototype.InitCurrentClass = function (obj) //初始化tag样式表
        {

            var tags = this.GetTags();
            if (tags != null && tags.length > 0) {
                for (var i = 0; i < tags.length; i++) {
                    if (tags[i] != obj) {
                        tags[i].className = this.ClassName;
                    }
                }
            }

            obj.className = this.CurrentClassName;

        }
        CustomTags.prototype.InitCurrent = function () //跨页tag初始化
        {
            var CurrentTagName = GetUrlParams("tagname");
            var obj = null;
            var tags = this.GetTags();
            for (var i = 0; i < tags.length; i++) {

                if ($(tags[i]).attr("name") == CurrentTagName) {
                    obj = tags[i];
                    break;
                }
            }
            if (obj == null)
                obj = tags[0];

            this.InitCurrentClass(obj);
        }
        CustomTags.prototype.InitOnclick = function (index) {
            var tags = this.GetTags();
            var obj = tags[index];
            if (obj == "undefined" || obj == null) {
                //alert("没有找到对应的Tag");
                return;
            }
            $(obj).click();
        }
        CustomTags.prototype.GetTags = function () {

            if (this.TagsList == null) {
                var Tags = [];
                var isid = (this.ParentObjName.charAt(0) != ".") ? "#" + this.ParentObjName : this.ParentObjName;

                $(isid).find(this.SubObj).each(
                    function (i) {
                        Tags.push(this);
                        $(this).css("cursor", "pointer");
                    }
                );
                this.TagsList = Tags;
            }
            return this.TagsList;
        }
    }
    CustomTags._initialized = true;

}


$(function(){
    var TopTags = new CustomTags();
    TopTags.ParentObjName = "panrent-menu";
    TopTags.SubObj = "span";
    TopTags.CurrentClassName = "current";
    TopTags.ClassName = "";

    TopTags.fun = OnMainTags; // function () { OnMainTags(this) };

    TopTags.InitOnclickInTags();

    TopTags.InitOnclick(0);
})


function OnMainTags(obj) {
     
    var sID = $(obj).data("mid");
    GetMenus(sID);

}

function GetMenus(MenuParentID) { 
    LeftMenuList.innerHTML = "<div><img height='250px' src='../images/loading.gif' /></div>";
    let prams = {"pid":MenuParentID}
    post_form("/api/getsubmenus", prams, CompGetMenus);
}
function CompGetMenus(msg) {
    var aMenus = msg.data;//eval(msg);
    if (aMenus == null || aMenus == undefined || aMenus.length < 1) {
        LeftMenuList.innerHTML = "<font color='red'>您还没有安装任何模块</font>";
        return;
    }
    var sbMenuList = new StringBuilder();
    sbMenuList.Append("<table id=\"tdMenuList\"  border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" >");
    for (var i = 0; i < aMenus.length; i++) {
        var CurrentMenu = aMenus[i];

        sbMenuList.Append("<tr onclick=\"OnMenuTitle(this)\"><td  class=\"treeview_unfocus\">");
        sbMenuList.Append("<i class='"+CurrentMenu.img+"' /></i>&nbsp;");
        sbMenuList.Append(CurrentMenu.MenuTitle);
        sbMenuList.Append("</td></tr><tr><td><div  class=\"BasicinfoShow\"><ul>");
        sbMenuList.Append(BindLeftMenuItems(CurrentMenu.Items));
        sbMenuList.Append("</ul></div></td></tr>");
    }
    sbMenuList.Append("</table>");
    LeftMenuList.innerHTML = sbMenuList.toString();

    $(".menu-click").click(function () {
        $(".menu-title span").text($(this).text());
    });

}

function BindLeftMenuItems(Items) {
    var sbItems = new StringBuilder();
    // alert(Items)
    for (var i = 0; i < Items.length; i++) {
        var CurrentItem = Items[i];
        sbItems.Append("<li data-id='"+CurrentItem.id+"' data-href='"+CurrentItem.url+"' data-txt='"+CurrentItem.ItemName+"' onclick='OnSubMenu(this)'>");
        sbItems.Append("<a class='menu-click'");
        sbItems.Append("  href=\"");
        sbItems.Append(CurrentItem.url);
        sbItems.Append("\" target=rform");
        sbItems.Append(" >");
        sbItems.Append("<i class='"+CurrentItem.img+"' /></i>&nbsp;");
        sbItems.Append(CurrentItem.ItemName);
        sbItems.Append("</a></li>");
    }
    return sbItems.toString();
}

function OnSubMenu(ob) {
    $("#LeftMenuList").find("li").each(
		function (i) {
		    $(this).attr("class", "");
		}
    ); 
    $(ob).attr("class", "selectThisItemsStyle");
}
function OnMenuTitle(ob) {
    var onTitle = $(ob);
    var IsOpen = onTitle.attr("isop");
    var onNext = onTitle.next();
    if (IsOpen == null || IsOpen == undefined || IsOpen == "1") {
        onNext.hide();
        onTitle.attr("isop", "0");
    }
    else {
        onNext.show();
        onTitle.attr("isop", "1");
        
    }
}

function OpenLeftMenu() {
    //thisID = document.getElementById(thisID);
    var ob = $("#leftList")
    var tg = ob.attr("tg"); 
    if (tg == null || tg == undefined || tg == 1) {
        ob.fadeOut("slow");
        ob.attr("tg", "0"); 
    }
    else {
        ob.fadeIn("slow");
        ob.attr("tg", "1"); 
    } 
}

function del_items(url) {
        var ids = get_checkboxval(".eb-table");
        if (ids)
            location.href = url+'?ids=' + ids;
        else
            alert("请选择要删除的数据！");
    }