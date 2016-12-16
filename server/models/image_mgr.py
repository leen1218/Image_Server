# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Dec 16, 2016
#

from utils.logger_helper import logger
from qiniu import Auth
import urllib

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

	# 七牛上传的空间
	_bucket_domain = 'oi2mkhmod.bkt.clouddn.com'

	_weixin_image_download_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

	_image_queue = []
	def __init__(self):
		pass

	def addImage(self, image):
		url = self._weixin_image_download_url % (image["token"], image["id"])
		local_path = image["local_path"]
		urllib.urlretrieve(url, local_path)
		# self._image_queue.append(image)

	def downloadAndUploadImage(self):
		pass
