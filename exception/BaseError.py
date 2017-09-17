#!/usr/bin/python
# encoding:utf-8


class BaseError(Exception):
    """
        所有已知异常
    """

    def __init__(self, status, err_msg):
        self.status_code = status
        self.err_msg = err_msg

    def __repr__(self):
        return u'StatusCode: %s, Message: %s' % (self.status_code, self.err_msg)

    def __str__(self):
        return self.__repr__()


