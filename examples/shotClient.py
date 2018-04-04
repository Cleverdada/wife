#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import time
import urllib


class OneServiceClient(object):
    url_prefix = "https://oneshot.alibaba-inc.com"

    def __init__(self):
        pass

    def _request(self, url, param=None, payload=None):
        if not payload:
            payload = {}
        if not param:
            param = {}
        param['_t'] = time.time()

        headers = {
            'Content-type': 'application/json;charset=gb2312',
            "User-Agent": "oneService-sdk"
        }

        try_count = 0
        result = {}
        while True:
            try:
                params = u'%s' % urllib.urlencode(param)
                _url = "%s?%s" % (url, params)
                if payload:
                    res = requests.post(_url, data=payload, headers=headers, verify=False)
                else:
                    res = requests.get(_url, headers=headers, verify=False)

                if res.status_code != 200:
                    raise Exception(res)
                print res.text
                result = json.loads(res.text)
                break
            except IOError, e:
                try_count += 1
                print u'can not connect to server, retry ... | reason: %s' % str(e)
                raise e
            except Exception, e:
                raise e

        if result['code'] != 0:
            error_msg = "{api}\nstatus: {status}\nerror_str: {errstr}".format(
                api='/'.join(url.split('/')[-2:]),
                status=result['code'],
                errstr=result['message'].encode('utf-8'),
            )
            raise Exception(error_msg)

        print u'api:%s request success  data:\n %s' % ('/'.join(url.split('/')[-2:]), json.dumps(result['data']))
        return result['data']

    def asyncShot(self):
        url = "%s%s" % (self.url_prefix, "/api/sst/task")
        payload = {"config":
                       {"device": "PC",
                        "fullPage": True,
                        "url": "http://www.baidu.com/",
                        "ttl": 1,
                        "format": "png",
                        "deviceScaleFactor": 1,
                        "bucMode": "none",
                        "viewport": "1440x800",
                        "isSync": 0
                        },
                   "from": "official",
                   "workId": "160926",
                   "pid": "test",
                   "token": "jphe58iy1nby714jzdgp1f9d1fzp5yli"
                   }
        return self._request(url, payload=json.dumps(payload))


    def syncShot(self):
        url = "%s%s" % (self.url_prefix, "/api/sst/screenshot")
        payload = {"config":
                       {"device": "PC",
                        "fullPage": True,
                        "url": "http://www.baidu.com/",
                        "format": "png",
                        "deviceScaleFactor": 1,
                        "bucMode": "none",
                        "viewport": "1440x800",
                        "isSync": 0
                        },
                   "pid": "test",
                   "token": "jphe58iy1nby714jzdgp1f9d1fzp5yli"
                   }
        return self._request(url, payload=json.dumps(payload))

if __name__ == '__main__':
    client = OneServiceClient()
    client.asyncShot()
    # client.syncShot()
