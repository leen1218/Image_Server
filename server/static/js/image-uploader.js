/**
 * Created by yunfei on 8/31/15.

 * 依赖: $.ajax, $.Deferred from <zepto.js or jquery.js>
 */

function getBase64Image(base64) {
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	var img = document.getElementById(base64);
	ctx.drawImage(img, 50, 50);
	alert("HERE!!"+ base64);
	dataURL = c.toDataURL("image/jpg");
	alert(dataURL);
  return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

function base64ToBinary(b64Data, sliceSize) {
    sliceSize = sliceSize || 512;
    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    var i;
    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }
    return byteArrays;
}


var QINIU_UPLOAD_HOST = 'http://upload.qiniu.com',
	qiniuTokens = {
		_tokens: {},

		getToken: function (url) {
		alert("getToken:" + url);
				return $.ajax({
					url: url
				}).then(function (data) {
				alert("uptoken:" + data.uptoken);
					return data.uptoken;
				});
		}
	};

function ImageUploader(config) {
	this.tokenUrl = config.tokenUrl;
	if (!this.tokenUrl) {
		throw new Error('Token URL is required for ImageUploader.');
	}
}

/**
 * @typedef {object} StringFile
 * @property {string} fileBase64 - the file data in base64 form
 * @property {string} key - the file name of the uploaded file
 */
/**
 * @params {{StringFile} | Array.<{StringFile}>} files
 */
ImageUploader.prototype.upload = function (files) {
	function uploadFileData(token, data, key) {
		alert("uploadFileData:" + key);
		var blockSize = 4 * 1024 * 1024, // 七牛上传要求单个块大小固定为4M(除最后一块)
			sliceNum = 256, // 块内分片数量，对应分片大小16384byte（可配置，但需保证划分后每个分片大小为整数）
			sliceBuffers = base64ToBinary(data, blockSize / sliceNum).map(function (typedArray) {
				return typedArray.buffer;
			}),
			blocks = [];
		for (var i = 0; i < sliceBuffers.length / sliceNum; i++) {
			blocks.push(sliceBuffers.slice(i * sliceNum, (i + 1) * sliceNum));
		}
		var sliceUploadedSizes = {},
			authHeader = {Authorization: 'UpToken ' + token},
			buffersSize = function (buffers) {
				return buffers.reduce(function (sum, buffer) {
					return sum + buffer.byteLength;
				}, 0);
			},
			sendBlock = function (blockSlices, blockIndex) {
			alert("sendBlock:" + blockSlices);
				var sendSlice = function (sliceConfig) {
						return $.ajax({
							type: 'POST',
							url: sliceConfig.url,
							data: sliceConfig.buffer,
							processData: false,
							contentType: false,
							headers: authHeader,
							error: function(xhr) {alert(JSON.stringify(xhr));},
							xhr: function () {
								var xhr = $.ajaxSettings.xhr();
								alert("sendSlice ajax:" + sliceConfig.url + xhr);
								// xhr.upload.addEventListener('progress', function (e) {
								// 	alert("sendSlice ajax:" + sliceConfig.url + "back"+ xhr);
								// 	sliceUploadedSizes[sliceConfig.sliceKey] = e.loaded;
								// });
								return xhr;
							}
						});
					},
					promise = sendSlice({
						url: QINIU_UPLOAD_HOST + '/mkblk/' + buffersSize(blockSlices),
						buffer: blockSlices[0],
						sliceKey: blockIndex + '_' + 0
					}),
					sliceSender = function (sliceIndex) {
						return function (data) {
							alert("send slice " + sliceIndex);
							return sendSlice({
								url: [QINIU_UPLOAD_HOST, 'bput', data.ctx, data.offset].join('/'),
								buffer: blockSlices[sliceIndex],
								sliceKey: blockIndex + '_' + sliceIndex
							});
						};
					};
				for (var i = 1; i < blockSlices.length; i++) {
					promise = promise.then(sliceSender(i));
				}
				return promise.then(function (data) {
					alert("THe promise finished with data.ctx:" + data.ctx);
					return data.ctx;
				}).catch(function (err) {alert(err);});
			};

		return $.when.apply($, blocks.map(sendBlock))
			.then(function () {
				alert("ajax send mkfile command");
				return $.ajax({
					type: 'POST',
					url: [QINIU_UPLOAD_HOST, 'mkfile', buffersSize(sliceBuffers), 'key', btoa(key)].join('/'),
					data: Array.prototype.join.call(arguments, ','),
					headers: authHeader,
					error: function(xhr) {alert(JSON.stringify(xhr));}
				});
			});
	}

	return qiniuTokens.getToken(this.tokenUrl)
		.then(function (token) {
			alert("getToken->then()" + token);
			files = [].concat(files);
			return $.when.apply($, files.map(function (file) {
				alert("getToken->then()->uploadFileData" + file.key);
				return uploadFileData(token, file.fileBase64, file.key);
			}));
		}).then(function (data) {
			alert("getToken->then()->2");
			var keys = [].map.call(arguments, function (a) {
				return {name: a.key};
			});
			return keys.length > 1 ? keys : keys[0];
		});
};

function uploadImages(images) {
	window.onerror = function(e) {alert(JSON.stringify(e));}
			var baseUrl = "https://www.yixiuhz.top/imageUploader/upToken?imageURL=";
			alert("1");
			var imageUploader = new ImageUploader({
					tokenUrl: '/j/qiniu/photo_token'
				});
			alert("2");
			var notUploadedImages = images.filter(function (image) {
				return !image.name;
			});
			alert("3");

			return $.when.apply($, notUploadedImages.map(function (image) {
				var base64 = image.base64,
					key = 'web' + Date.now();
					alert("ImageId:" + image.id);
					imageUploader.tokenUrl = baseUrl + key;

				return imageUploader.upload({
					fileBase64: getBase64Image(base64),
					key: key
				}).then(function () {
					image.base64 = '';
					image.name = key;
					alert("success!!");
				});
			})).fail(function () {
				alert("fail!!");
			}).always(function () {
				alert("always!!");
			});
		}

