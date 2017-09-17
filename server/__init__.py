#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask

from static import template_path, static_path

__author__ = 'kongchao'

app = Flask(__name__, template_folder=template_path, static_folder=static_path)

import server.views
import server.handler