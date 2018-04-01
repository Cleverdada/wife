#!/usr/bin/python
# -*- coding: utf-8 -*-

from examples.sdk import OneServiceClient


def get_hbaseColumns():
    hbaseColumns = list()
    for i in range(1):
        columnName = "field_name" + str(i)
        hbaseColumn = {
            "columnMapping": "info:%s" % columnName,
            "columnName": columnName,
            "columnType": "String",
            "columnCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
            "des": "desc_" + columnName,
            "route": None,
            "rowState": 3
        }
        hbaseColumns.append(hbaseColumn)
    return hbaseColumns


def get_hbaseRowkeys():
    hbaseRowkeys = list()
    for i in range(1):
        rowkeyName = "rowkey_name" + str(i)
        hbaseRowkey = {
            "rowKeyName": rowkeyName,
            "rowkeyType": "String",
            "preSuffix": "none",
            "rowkeyCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
            "needful": False,
            "des": "desc_" + rowkeyName,
            "rowState": 3
        }
        hbaseRowkeys.append(hbaseRowkey)
    return hbaseRowkeys


def get_hbaseMeta(adminName, adminId, db_id, hbase_phys_name):
    hbaseMeta = {
        "adminName": adminName,
        "adminId": adminId,
        "dbId": db_id,
        "tableName": hbase_phys_name,
        "isRealTime": False,
        "rowCoder": "com.alibaba.china.dw.dataopen.andor.rowcoder.IPageRowCoder",
        "hbaseRowkeys": get_hbaseRowkeys(),
        "hbaseColumns": get_hbaseColumns()
    }
    import json
    print json.dumps(hbaseMeta)
    return hbaseMeta

def get_hbaseMeta_bak():
    return {
        "adminName": "孔超(饸饹)",
        "adminId": "160926",
        "dbId": 4, "tableName": "hbase_phys_name36",
        "isRealTime": False,
        "hbaseColumns": [
            {
                "columnMapping": "info:adasdf",
                "columnName": "sdfadsg",
                "columnType": "String",
                "columnCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
                "des": "sfadsf",
                "rowState": 3}],
        "hbaseRowkeys": [
            {"rowKeyName": "sfadf",
             "rowkeyType": "String",
             "preSuffix": "none",
             "rowkeyCoder": "com.taobao.ustore.repo.hbase.DefaultColumnCoder",
             "needful": False,
             "des": "adfdsf",
             "rowState": 3
             }
        ],
        "rowCoder": "com.alibaba.china.dw.dataopen.andor.rowcoder.IPageRowCoder"
    }

def deploy_phys(hbaseMeta):
    client.existHbaseTable(hbase_phys_name)

    table_id = client.insertSubmitAllNoApp(hbaseMeta)
    # client.getTable(table_id)
    tables = client.listHbaseDeploy(hbaseTableName=hbase_phys_name, isOnline=0)
    Id = tables[0]['id']
    client.deploy(Id, isOnline=0)
    client.deploy(Id, isOnline=1)

def deploy_logic(hbase_phys_name, db_id):
    # 逻辑表英文名
    en_logic_table_name = "en_logic_name"
    # 逻辑主键英文名
    logic_pk_name = "en_pk_name"

    logic_table = {"logicTable":
                       {"cn": "逻辑中文表名",
                        "en": en_logic_table_name,
                        "ownerId": "160926",
                        "ownerName": "孔超(饸饹)",
                        "adminId": "160926",
                        "adminName": "孔超(饸饹)",
                        "department": "TMALL",
                        "topicId": 1000060,
                        "limitCnt": 1440},
                   "logicKeys": [
                       {
                           "en": logic_pk_name,
                           "cn": "中文_pk_name",
                           "isRequire": False,
                           "rowState": 3
                       }]
                   }
    logic_table_id = client.saveDraft(logic_table)
    phy_cols = client.listMetabyName(tableName=hbase_phys_name, dbId=db_id)

    physTableMeta = {
        "physCols": [
            {
                "logicTableId": logic_table_id,
                "cn": "desc_rowkey_name0",
                "en": "rowkey_name0",
                "text": logic_pk_name,
                "value": logic_pk_name,
                "rowState": 3,
                "isKey": True,
                "logicColName": logic_pk_name,
                "type": "String",

                "auditorId": None,
                "auditorName": None,
                "creatorId": None,
                "creatorName": None,
                "deployerId": None,
                "deployerName": None,
                "des": None,
                "gmtCreate": None,
                "gmtDeploy": None,
                "gmtModified": None,
                "id": None,
                "isRequire": False,
                "lastOpId": None,
                "lastOpName": None,
                "sequenceDao": None,
                "status": None,
                "logicColId": None,
                "needRename": None,
                "physTableId": None,
                "physTableName": None,
            },

            {
                "text": "不关联",
                "value": "no-bind-key",
                "cn": "desc_field_name0",
                "type": "String",
                "rowState": 3,
                "logicColName": "logic_field_name0",
                "en": "field_name0",

                "auditorId": None,
                "auditorName": None,
                "creatorId": None,
                "creatorName": None,
                "deployerId": None,
                "deployerName": None,
                "des": None,
                "gmtCreate": None,
                "gmtDeploy": None,
                "gmtModified": None,
                "id": None,
                "isKey": False,
                "isRequire": False,
                "lastOpId": None,
                "lastOpName": None,
                "logicColId": None,
                "needRename": None,
                "physTableId": None,
                "physTableName": None,
                "sequenceDao": None,
                "status": None
            }
        ],
        "physTable": {
            "cache":
                {"isCache": False},
            "db": {"text": "ipage", "value": 5},
            "en": hbase_phys_name,
            "logicTableId": logic_table_id,
            "isCache": False,
            "dbId": db_id}
    }

    logic_deploy_id = client.saveTable(physTableMeta)

    client.saveSubmit(logic_table_id)
    client.deploy(logic_deploy_id, 0)
    client.deploy(logic_deploy_id, 1)


if __name__ == '__main__':
    # 发布物理表流程
    client = OneServiceClient("os_QmbaMxhutWCQAjGXKc12FqMPp7xHSwwUzizggbFBwCTiq5", "160926")
    # # db_id
    db_name = 'ipage'
    dbs = client.listDb()
    db_ids = [db['id'] for db in dbs if db['name'] == db_name]
    db_id = db_ids[0]

    # 物理表名
    hbase_phys_name = "hbase_phys_name42"

    hbaseMeta = get_hbaseMeta(adminName="孔超(饸饹)", adminId="160926", db_id=db_id, hbase_phys_name=hbase_phys_name)
    deploy_phys(hbaseMeta)

    deploy_logic(hbase_phys_name, db_id)

