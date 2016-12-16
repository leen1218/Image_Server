# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 9, 2016
#

import tornado

class BaseHandler(tornado.web.RequestHandler):

	@property
	def db(self):
		return self.application.db

	@property
	def model(self):
	    return self.application.model

	@property
	def appSetting(self):
		return self.application.settings