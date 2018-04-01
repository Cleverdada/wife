#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import time
import urllib


class OneServiceClient(object):
    url_prefix = "http://oneservice.alibaba-inc.com/v2"

    def __init__(self, token, emp_id):
        self.token = token
        self.emp_id = emp_id

    def _request(self, url, param=None, payload=None):
        if not payload:
            payload = {}
        if not param:
            param = {}
        param['_t'] = time.time()
        param['os_access_token'] = self.token
        # todo: change workNo to emp_id
        param['os_emp_id'] = self.emp_id

        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
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

    def existHbaseTable(self, tableName):
        url = "%s%s" % (self.url_prefix, "/hbasetable/existHbaseTable.json")
        param = {
            "tableName": tableName
        }
        return self._request(url, param)

    def getModulesCount(self):
        url = "%s%s" % (self.url_prefix, "/custom/getModulesCount.json")
        return self._request(url)

    def listMyHbaseTable(self):
        url = "%s%s" % (self.url_prefix, "/custom/listMyHbaseTable.json")
        return self._request(url)

    def listDb(self):
        url = "%s%s" % (self.url_prefix, "/type/listDb.json")
        return self._request(url)

    def listEmp(self):
        url = "%s%s" % (self.url_prefix, "/user/listEmp.json")
        param = {
            "keyword": "160926"
        }
        return self._request(url, param=param)

    def listColType(self):
        url = "%s%s" % (self.url_prefix, "/type/listColType.json")
        return self._request(url)

    def listColumnCoder(self):
        url = "%s%s" % (self.url_prefix, "/type/listColumnCoder.json")
        return self._request(url)

    def listRowCoder(self):
        url = "%s%s" % (self.url_prefix, "/type/listRowCoder.json")
        return self._request(url)

    def listHbaseDeploy(self, hbaseTableName, isOnline):
        url = "%s%s" % (self.url_prefix, "/pub/listHbaseDeploy.json")
        param = {
            "hbaseTable": hbaseTableName,
            "isOnline": isOnline
        }
        return self._request(url, param)

    def updateSubmitAllNoApp(self):
        url = "%s%s" % (self.url_prefix, "/hbasetable/updateSubmitAllNoApp.json")
        hbaseMeta = {"adminName": "孔超(饸饹)",
                     "adminId": "160926",
                     "dbId": 4,
                     "tableName": "dadfad",
                     "isRealTime": False,
                     "hbaseColumns": [
                         {
                             "columnMapping": "info:",
                             "columnName": "sdfasd",
                             "columnType": "String",
                             "columnCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
                             "des": "daf",
                             "route": None,
                             "rowState": 1,
                             "id": 184809
                         }
                     ],
                     "hbaseRowkeys": [
                         {
                             "rowKeyName": "info:name",
                             "rowkeyType": "String",
                             "preSuffix": "none",
                             "rowkeyCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
                             "needful": False,
                             "des": "asdasf",
                             "rowState": 3
                         }
                     ],
                     "rowCoder": "com.alibaba.china.dw.dataopen.andor.rowcoder.IPageRowCoder",
                     "rowState": 0,
                     "tableId": 8585
                     }
        payload = {"hbaseMeta": json.dumps(hbaseMeta)}
        return self._request(url, payload=payload)

    def insertSubmitAllNoApp(self, hbaseMeta):
        """
               hbaseMeta = {"adminName": "孔超(饸饹)",
                            "adminId": "160926",
                            "dbId": 4,
                            "tableName": "dadfad",
                            "isRealTime": False,
                            "hbaseColumns": [
                                {
                                    "columnMapping": "info:",
                                    "columnName": "sdfasd",
                                    "columnType": "String",
                                    "columnCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
                                    "des": "daf",
                                    "route": None,
                                    "rowState": 1,
                                }
                            ],
                            "hbaseRowkeys": [
                                {
                                    "rowKeyName": "info:name",
                                    "rowkeyType": "String",
                                    "preSuffix": "none",
                                    "rowkeyCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
                                    "needful": False,
                                    "des": "asdasf",
                                    "rowState": 3
                                }
                            ],
                            "rowCoder": "com.alibaba.china.dw.dataopen.andor.rowcoder.IPageRowCoder",
                            "rowState": 0,
                            }
               """
        url = "%s%s" % (self.url_prefix, "/hbasetable/insertSubmitAllNoApp.json")
        payload = {"hbaseMeta": json.dumps(hbaseMeta)}
        return self._request(url, payload=payload)

    def deleteHbaseTable(self):
        url = "%s%s" % (self.url_prefix, "/hbasetable/deleteTable.json")
        param = {
            "id": 8586,
        }
        return self._request(url, param)

    def getTable(self, id):
        url = "%s%s" % (self.url_prefix, "/hbasetable/getTable.json")
        param = {
            "id": id,
        }
        return self._request(url, param)

    def deploy(self, ids, isOnline):
        url = "%s%s" % (self.url_prefix, "/pub/deploy.json")
        param = {
            "ids": ids,
            "isOnline": isOnline
        }
        return self._request(url, param)

    def listLogicByPk(self):
        url = "%s%s" % (self.url_prefix, "/logic/listLogicByPk.json")
        param = {
            "keyCols": "adasfa",
        }
        return self._request(url, param)

    def listTopic(self):
        url = "%s%s" % (self.url_prefix, "/topic/listTopic.json")
        return self._request(url)

    def listDepartment(self):
        url = "%s%s" % (self.url_prefix, "/user/listDepartment.json")
        return self._request(url)

    def saveDraft(self, logic_table):
        url = "%s%s" % (self.url_prefix, "/logic/saveDraft.json")
        payload = {"logicMeta": json.dumps(logic_table)}
        return self._request(url, payload)

    def getLogicTableBaseInfo(self):
        url = "%s%s" % (self.url_prefix, "/logicTableView/getLogicTableBaseInfo.json")
        param = {
            "tableId": "1025257",
        }
        return self._request(url, param)

    def listPhysTables(self):
        url = "%s%s" % (self.url_prefix, "/logic/listPhysTables.json")
        param = {
            "id": "1025257",
        }
        return self._request(url, param)

    def listMetabyName(self, tableName, dbId):
        url = "%s%s" % (self.url_prefix, "/phys/listMetabyName.json")

        param = dict(
            tableName=tableName,
            dbId=dbId
        )
        return self._request(url, param)

    def saveTable(self, physTableMeta):
        url = "%s%s" % (self.url_prefix, "/phys/saveTable.json")
        payload = {"physTableMeta": json.dumps(physTableMeta)}
        return self._request(url, payload)

    def saveSubmit(self, logic_table_id):
        url = "%s%s" % (self.url_prefix, "/logic/saveSubmit.json")
        logicMeta = {
            "logicTable":
                {"id": logic_table_id},
            "logicKeys": []
        }
        payload = {"logicMeta": json.dumps(logicMeta)}
        return self._request(url, payload)

    def listAllDeploy(self):
        url = "%s%s" % (self.url_prefix, "/pub/listAllDeploy.json")
        param = {"logicTableId": 1025261,
                 "isOnline": 0}

        return self._request(url, param)


if __name__ == '__main__':
    client = OneServiceClient("os_QmbaMxhutWCQAjGXKc12FqMPp7xHSwwUzizggbFBwCTiq5", "160926")
    client.existHbaseTable("testh")
    client.getModulesCount()
    client.listMyHbaseTable()
    client.listDb()
    # listEmp日常会有超时，先注释掉
    # client.listEmp()
    client.listColType()
    client.listColumnCoder()
    client.listRowCoder()
    client.listHbaseDeploy('testh', 0)

    # client.updateSubmitAllNoApp()
    # client.insertSubmitAllNoApp()
    # client.deleteHbaseTable()
    # client.deploy()

    client.listLogicByPk()
    # client.listTopic()
    client.listDepartment()
    # client.saveDraft()
    client.getLogicTableBaseInfo()
    client.listPhysTables()
    client.listHbaseDeploy('testh', 1)
    # client.listMetabyName()
    # client.saveSubmit()
    # client.saveTable()
    client.listAllDeploy()





