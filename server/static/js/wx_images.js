/**
 * Created by bhuang on 12/15/16.
 */

var imageIds = [];
var chooseAndUploadImage = function() {
    alert("chooseAndUploadImage");
    wx.chooseImage({
        count: 2, // 默认9
        sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
        sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
        success: function (res) {
            var localIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
            var uploadImageToWx = function(i, callback) {
                if (i >= localIds.length) {
                    return;
                }
                $("#uploadImages").append("<img src=" + localIds[i] + " width='200' height='200' />");
                wx.uploadImage({
                    localId: localIds[i], // 需要上传的图片的本地ID，由chooseImage接口获得
                    isShowProgressTips: 0, // 默认为1，显示进度提示
                    success: function (res) {
                        var serverId = res.serverId; // 返回图片的服务器端ID
                        alert("image" + localIds[i] + ": " + serverId);
                        imageIds.push(serverId);
                        callback.apply(null, [i + 1, callback]);
                    }
                });
            };

            uploadImageToWx(0, uploadImageToWx);


            /*for (var i = 0; i < localIds.length; ++i) {
                $("#uploadImages").append("<img src=localIds[i] />");
                wx.uploadImage({
                    localId: localIds[i], // 需要上传的图片的本地ID，由chooseImage接口获得
                    isShowProgressTips: 0, // 默认为1，显示进度提示
                    success: function (res) {
                        var serverId = res.serverId; // 返回图片的服务器端ID
                        alert(serverId);
                        imageIds.push(serverId);
                    }
                });
            }*/
            /*$("#uploadImages").append("<img src=" + localIds[0] + " width='100px' height='100px' />");
            $("#uploadImages").append("<img src=" + localIds[1] + " width='100px' height='100px' />");
                wx.uploadImage({
                    localId: localIds[0], // 需要上传的图片的本地ID，由chooseImage接口获得
                    isShowProgressTips: 0, // 默认为1，显示进度提示
                    success: function (res) {
                        var serverId = res.serverId; // 返回图片的服务器端ID
                        alert("upload image1: " + serverId);
                        imageIds.push(serverId);
                        wx.uploadImage({
                            localId: localIds[1], // 需要上传的图片的本地ID，由chooseImage接口获得
                            isShowProgressTips: 0, // 默认为1，显示进度提示
                            success: function (res) {
                                var serverId = res.serverId; // 返回图片的服务器端ID
                                alert("upload image2: " + serverId);
                                imageIds.push(serverId);

                            }
                        });
                    }
                });*/
        }
    });
}

var submitOrder = function () {
    alert("ImageIds:" + imageIds[0] + " AND " + imageIds[1]);
    $("#loader").css("display", "block");
    $("#mask").css("display", "block");


    $.ajax({
        async: false,
        url: "https://www.yixiuhz.top/imageUploader/upload",
        data: JSON.stringify({"media_ids": imageIds}),
        type: "POST",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        timeout: 8000,
        success: function(result){
            alert(JSON.stringify(result));
            $("#loader").css("display", "none");
            $("#mask").css("display", "none");
        },
        error: function(xhr) {
            $("#loader").css("display", "none");
            $("#mask").css("display", "none");
            alert("An error occured: " + xhr.status + " " + xhr.statusText);
        }
    });
}