# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 9, 2016
#
import os

from tornado import web
from tornado.ioloop import IOLoop
from tornado.options import options

from libs import options as myOptions
from models import model
from handlers import config_pattern

class Application(web.Application):
    def __init__(self, model):

		self.model = model

		#config setting from options
		settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"), cookie_secret=options.cookie_secret, static_path=os.path.join(os.path.dirname(__file__), "static"))

		#setup DB
		# self.db = torndb.Connection("%s:%s" % (options.mysql["host"], options.mysql["port"]), options.mysql["database"], user=options.mysql["user"], password=options.mysql["password"], charset='utf8')

		#handlersPattern
		handlers = config_pattern.handlersPattern
		super(Application, self).__init__(handlers, **settings)

if __name__ == '__main__':
	myOptions.parse_options()
	app = Application(model.Model())
	app.listen(options.port)

	IOLoop.instance().start()
