#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import send_from_directory, request

from server import app
from static import template_path, static_path, cache_path


@app.route('/<path>', methods=['GET'])
def index(path):
    if not path:
        path = 'index.html'
    if path.endswith('css'):
        mimetype = 'application/x-css'
    else:
        mimetype = None
    return send_from_directory(template_path, path, mimetype=mimetype)


@app.route('/mail', methods=['GET'])
def mail():
    print "mail has read"
    return ""


@app.route('/shot', methods=['GET'])
def shot():
    print "shot success"
    return ""


@app.route('/', methods=['GET'])
def home():
    return send_from_directory(template_path, 'index.html')
