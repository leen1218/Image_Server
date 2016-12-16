# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 en li. All rights reserved.
#
# @author: En Li <hunterli1218@gmail.com>
# Created on  Nov 9, 2016
#

import os

from tornado.options import parse_command_line, options, define

def parse_config_file(path):
    """Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.
    """
    config = {}
    execfile(path, config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


def parse_options():
    _root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    _settings = os.path.join(_root, "settings.py")
    parse_config_file(_settings)

    parse_command_line()
