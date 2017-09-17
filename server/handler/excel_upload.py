# coding: utf-8
import os
from flask import request, session, jsonify
from server import app
from static import cache_path

__author__ = 'kongchao'
__email__ = 'ggc0402@qq.com'


@app.route('/api/excel/upload', methods=['post'])
def excel_upload():
    print 'hehe'
    f = request.files['file']
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    upload_path = os.path.join(cache_path, 'opends.conf')
    f.save(upload_path)
    res = {"res": "hehe"}
    # os.remove(upload_path)
    return jsonify(res)
