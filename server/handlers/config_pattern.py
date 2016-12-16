# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 9, 2016
#

from handlers.imageLoader.upload_image import UploadImage


handlersPattern = [
				   # 七牛图片服务器
				   (r'/imageUploader/upload', UploadImage),
				   ]
