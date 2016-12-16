# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 23, 2016
#

"""Global Model Instance"""
import image_mgr

class Model():
	def __init__(self):
		self.image_mgr = image_mgr.ImageManager()