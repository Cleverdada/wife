#!/usr/bin/python
# encoding:utf-8
import xlrd

from util.mysql import connection


class ExcelImport(object):
    def get_excel_data(self, excel_path):
        return xlrd.open_workbook(excel_path, encoding_override="gbk")

    def validate_excel_header(self):
        pass

    def contact_sql(self):
        pass


if __name__ == '__main__':
    # in_path = "resource/考勤.xls"
    in_path = "/Users/HaiZhi/Desktop/9月考勤.xlsx"
    excel_import = ExcelImport()
    excel_data = excel_import.get_excel_data(in_path)
    sheet0 = excel_data.sheets()[0]
    print sheet0
    header = sheet0.row_values(0)
    header_templates = ["姓名", "登记号码", "日期时间"]
    create_sql = """
        drop table if EXISTS april;
        CREATE TABLE `april` (
          `姓名` varchar(255) DEFAULT NULL,
          `登记号码` varchar(255) DEFAULT NULL,
          `日期时间` varchar(255) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connection.cursor()
    cursor.execute("use mydb")
    cursor.execute(create_sql)
    cursor.close()

    cursor = connection.cursor()
    row_count = sheet0.nrows
    for i in range(row_count):
        if i == 0:
            continue
        else:
            sql = "insert into april values(%s, %s, %s)"
            print sql
            d = [sheet0.row_values(i)[0], sheet0.row_values(i)[1], sheet0.row_values(i)[2]]
            cursor.execute(sql, d)
    cursor.close()
    connection.commit()
    out_path = "resource/考勤处理.xls"

    cursor = connection.cursor()
    with open("scripts/mx_origin_create.sql", 'r') as f:
        cursor.execute(f.read())
        cursor.close()

    drop_table = "drop table if EXISTS mx_final;"
    cursor = connection.cursor()
    cursor.execute(drop_table)
    cursor.close()

    cursor = connection.cursor()
    with open("scripts/mx_final_create.sql", 'r') as f:
        cursor.execute(f.read())
        cursor.close()

    cursor = connection.cursor()
    with open("scripts/mx_out.sql", 'r') as f:
        cursor.execute(f.read())
        cursor.close()
