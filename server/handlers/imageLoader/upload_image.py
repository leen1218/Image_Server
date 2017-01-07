# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 9, 2016
#

from tornado import escape
from utils.logger_helper import logger
from handlers.base_handler import BaseHandler
import json


class UploadImage(BaseHandler):

	"""
	微信图片流程测试模块，接收微信图片media_id，由image manager负责下载和上传到七牛
	"""

	def get(self):
		response = {"msg": "请使用POST API"}
		response_json = json.dumps(response, encoding="UTF-8", ensure_ascii=False)
		self.write(response_json)

	def post(self):
		body = escape.json_decode(self.request.body)
		logger.debug("UploadImage : body = " + str(body))
		images = body["images"]
		token = body["token"]
		for image in images:
			image_d = {}
			image_d["id"] = image["id"]
			image_d["token"] = token
			image_d["local_path"] = self.settings["static_path"] + "/images/%s.jpg" % image["id"]
			image_d["save_path"] = image["save_path"]
			logger.debug("UploadImage : 图片 %s 添加到下载队列" % image["save_path"].encode("utf-8"))
			self.model.image_mgr.addImage(image_d)
		response = {"msg" : "图片已添加到下载队列"}
		response_json = json.dumps(response, encoding="UTF-8", ensure_ascii=False)
		self.write(response_json)




