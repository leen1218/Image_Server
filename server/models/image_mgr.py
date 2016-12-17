# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Dec 16, 2016
#

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from utils.logger_helper import logger
import urllib
import tornado
import os


"""Global Image Manager Instance"""

class ImageManager(object):

	"""
	图片管理类

	_image_queue		待下载图片队列

	addImage			添加图片到待下载队列
	@param(image) 		dict {id, key, url}

	downloadAndUploadImage	从微信服务器下载图片，并且上传到七牛服务器，通过定时器实现，每次下载一个，每一分钟进行一次
	"""

	# 七牛服务器 Access Key 和 Secret Key
	_access_key = 'l1NMMFf-xmqnqwQ3xibbiScwBjjZYHLiFIaTGFod'
	_secret_key = 'n0olj_tdl-QUeHRK8LqJ_xeoOKW8vfGEgYWiihvV'

	# 七牛上传的空间名字
	_bucket_name = 'zngj'

	# 七牛上传的空间域名
	_bucket_domain = 'oi2mkhmod.bkt.clouddn.com'

	_weixin_image_download_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

	# 图片队列，业务服务器添加图片到该待下载队列，由定时器负责下载
	_image_queue = []

	_upload_image_time_interval = 60 * 1000

	def __init__(self):
		self.start()

	def start(self):
		"""执行定时器任务"""
		logger.info('【图片服务器管理者】>>>执行定时器任务')
		tornado.ioloop.IOLoop.instance().call_later(0, self.downloadAndUploadImage)
		tornado.ioloop.PeriodicCallback(self.downloadAndUploadImage, self._upload_image_time_interval).start()

	def addImage(self, image):
		self._image_queue.append(image)

	# 定时器调用，因为目前跟业务服务器位于同一台云服务器，资源分配策略，每一分钟执行一次图片上传函数
	def downloadAndUploadImage(self):
		if len(self._image_queue) > 0:
			image = self._image_queue[0]
			if self.downloadImageFromWeChatServer(image):
				# 从微信服务器下载成功
				if self.uploadImageToQiniu(image):
					# 上传七牛服务器成功
					self._image_queue.remove(0)
					# 删除本地图片
					os.remove(image["local_path"])
					return True
				else:
					return False
			else:
				return False
		else:
			logger.debug("ImageManager : 没有待下载图片，图片服务器空闲！")
		return False


	def downloadImageFromWeChatServer(self, image):
		url = self._weixin_image_download_url % (image["token"], image["id"])
		local_path = image["local_path"]
		try:
			urllib.urlretrieve(url, local_path)
		except Exception:
			return False
		return True

	def	uploadImageToQiniu(self, image):
		# 构建鉴权对象
		q = Auth(self._access_key, self._secret_key)

		# 上传到七牛后保存的文件名
		key = '%s.jpg' % image["id"]

		# 生成上传 Token，可以指定过期时间等
		token = q.upload_token(self._bucket_name, key, 3600)

		# 要上传文件的本地路径
		localfile = image["local_path"]

		ret, info = put_file(token, key, localfile)
		if info["statuc_code"] == 200:
			logger.debug("ImageManager : upload local image" + localfile.encode("utf-8") + "to qiniu successfully, save as " + info["key"])
			return True
		else:
			return False


