#!/usr/bin/python
# encoding:utf-8

import MySQLdb
import MySQLdb.cursors as cursors

import util.config as config


def connect():
    input_info = config.get_section("connect_info")
    connect_info = dict(
        host=input_info.get('host'),
        port=int(input_info.get('port', 3306)),
        user=input_info.get('username'),
        passwd=input_info.get('password'),
        db=input_info.get('db'),
        # cursorclass=cursors.SSCursor,
        charset='utf8'
    )
    return MySQLdb.connect(**connect_info)


def create_cursor(connection):
    if connection:
        cursor = connection.cursor()
        return cursor

connection = connect()
