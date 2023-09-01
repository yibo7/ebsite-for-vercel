function InitFileUpload(filedata, fileList, inputid, isBatch) {
    ext = "zip,rar"
    sizeSingle = 10*1024;
    numLimit = 1000;// isBatch ? 1000 : 1;
    var uploader = WebUploader.create({
        auto: true,
        // swf文件路径
        //swf: SiteConfigs.UrlIISPath+'js/webuploader/Uploader.swf',
        //bdup不空服务端知道是来自百度的上传控件,只因这个控件的fileinput名称是写死的，所以要加个标记,后端除了这个地方，几乎是没有变动
        server: '/api/upfile?t=file',
        fileSingleSizeLimit: sizeSingle * 1024,//以ｋ为单位，限制上传单个文件大小 10*1024*1024,//限制大小10M
        fileNumLimit: numLimit,//上传数量限制
        fileSizeLimit: 1024 * 1024 * 100,//限制上传所有文件大小100M
        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: '#' + filedata,
        // 不压缩image, 默认如果是jpeg，文件上传前会压缩一把再上传！
        resize: false, 
        // 只允许选择图片文件。
        accept: {
            title: 'Images',
            extensions: 'png,jpeg,jpg,gif,rar,zip,txt,pdf,doc,docx,XLS,XLSX,PPT,PPTX,CSV,MP3,MP4,AVI,MOV,WMV',
            mimeTypes: '*/*'
        }
    });

    var $fileList = $("#" + fileList);
    var modifyVal = $("#" + inputid).val();
    if (modifyVal) {
        if (isBatch) {
            var aUrl = modifyVal.split(",");
            aUrl.map(function (item, index) {
                $fileList.append(getImgBox(item, item));
            });

        } else {
            $fileList.html(getImgBox(modifyVal, modifyVal));
        }
        updateValue();
    }
    // var $list = $("#thelist");
    // 当有文件被添加进队列的时候
    uploader.on('fileQueued', function (file) { 
        var $li = getImgBox(file.name);
        $li.attr("id", file.id); 
        if (isBatch) {
            $fileList.append($li);
        } else {
            $fileList.html($li); //只允许上传一个
        }
    });
    function getImgBox(showInfo, fileUrl) {
        var dataFile = '';
        if (fileUrl) {
            dataFile = 'data-file=' + fileUrl;
        }
        var item = $('<div ' + dataFile+' title="双击删除" class="fileitem">' +
            '<h4 class="info">' + showInfo + '</h4>' +
            '</div>'); 
        item.dblclick(function () {
            if (confirm('确认要删除当前项吗？')) {
                item.remove();
                updateValue();
            }
        });
        return item;
    }

    // 文件上传过程中创建进度条实时显示。
    uploader.on('uploadProgress', function (file, percentage) {
        //progress是html5特性
        var $li = $('#' + file.id),
            $percent = $li.find('progress');
        // 避免重复创建
        if (!$percent.length) {
            $percent = $('<progress value="0" max="100"></progress>').appendTo($li);//.find('span');
        }
        $percent.val(percentage * 100);
        $percent.text(percentage * 100 + '%');
        if (percentage == 1)
            $percent.remove()
    });
    uploader.on('uploadSuccess', function (file, response) {

        var data = response;
        if(data.state!="SUCCESS"){
            alert("upload err :"+data.state);
            return;
        }
        var uploadUrl = data.url;
        $('#' + file.id).addClass('upload-state-done');
        $('#' + file.id).data('file', uploadUrl);
        updateValue();
    });

    function updateValue() { 
        const aValue = [];
        $fileList.find('.fileitem').each(function () {
            var fileUrl = $(this).data('file'); 
            aValue.push(fileUrl)
        });
        $("#" + inputid).val(aValue.toString()); 
        //console.log(aValue.toString())
    }

    uploader.on('uploadError', function (file) {

        $('#' + file.id).find('p.state').text('远程地址返回错误信息');
    });
    uploader.on('error', function (errtype) {
        if (errtype == "Q_TYPE_DENIED") {
            alert("只允许上传格式" + ext);
        } else if (errtype == "Q_EXCEED_SIZE_LIMIT") {

            alert("所有文件大小不能超过100M");
        }
        else if (errtype == "F_EXCEED_SIZE") {
            var sizeMsg;
            if (sizeSingle < 1024)
                sizeMsg = sizeSingle + "KB";
            else
                sizeMsg = (sizeSingle / 1024) + "MB"
            alert("单个文件大小不能超过" + sizeMsg);
        }
        else if (errtype == "Q_EXCEED_NUM_LIMIT") {

            alert("文件数量不能超过" + numLimit); 
        }
        else if (errtype == "F_DUPLICATE") {

            alert("重复文件"); 
        }
        else {
            alert("上传出错！请检查后重新上传！错误代码" + errtype);
        }
    });

    uploader.on('uploadComplete', function (file) {
        $('#' + file.id).find('.progress').fadeOut();
    });
}