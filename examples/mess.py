#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import traceback
from email.mime.text import MIMEText  # 引入smtplib和MIMEText

import xlrd

SHEET_POSITION = 0
HEADER_OFFSET = 0
GROUP_INDEX = 1
EXCEPTION_INDEX = 11

SUBJECT = u"2018年03-04月份考勤核对表"

mail_info = dict(
    host='smtp.jszyfz.com',
    port=25,
    sender='zhanglin@jszyfz.com',
    pwd='xhwl20170327'
)

# observers = {
#     u"张琳": "zhanglin@jszyfz.com",
# }


def group(data):
    groups = {}
    for d in data:
        group_data = groups.get(d[GROUP_INDEX])  # type: list

        if group_data:
            group_data.append(d)
        else:
            group_data = []
            group_data.append(d)
        groups.update({d[GROUP_INDEX]: group_data})
    return groups


def parser(file_path):
    excel_data = []
    work_book = xlrd.open_workbook(file_path, encoding_override="utf-8")
    sheet = work_book.sheets()[SHEET_POSITION]
    header = sheet.row_values(HEADER_OFFSET)

    for row_index in range(sheet.nrows):
        if row_index <= HEADER_OFFSET:
            continue
        excel_data.append(sheet.row_values(row_index))
    return header, excel_data


def publish(header):
    observers = get_observers()
    for name, group_data in groups.iteritems():
        observer = observers.get(name)
        if not observer or name in ignored_list:
            print u"`%s` igored" % name
        else:
            try:
                mail_info.update({"receiver": observer,
                                  "body": gen_body(header, group_data)})
                send_mail(**mail_info)
                print u"`%s`, `%s` send success" % (name, observer)
            except Exception, e:
                print u"`%s`, `%s` send failed" % (name, observer)
                print traceback.format_exc()


def gen_body(header, group_data):
    body = u'<h1 align="center">2018年3月份考勤明细，请仔细核对，有异议请在4.2号5:00之前回复该邮件并且填写对应的申请单，找部门负责人签字后交给人力部—徐巧巧，没有问题的请忽略此邮件</h1>'
    body += '<table border="1" cellpadding="2" cellspacing="0" align="center" width="800px">'
    body += "<tr bgcolor='#eeccff'>"
    for h in header:
        body += "<td align='center'> <strong>%s</strong></td>" % h
    body += "</tr>"

    for i, r in enumerate(group_data):
        if not r[EXCEPTION_INDEX] or r[EXCEPTION_INDEX] == u'异常':
            r[EXCEPTION_INDEX] = u'异常'
            body += "<tr bgcolor='#FF0000'>"
            for c in r:
                body += "<td>%s</td>" % c
            body += "</tr>"
        else:
            bgcolor = "bgcolor = '#c7e5ff'" if i % 2 == 0 else "bgcolor = '#eaf5ff'"
            body += "<tr %s>" % bgcolor
            for c in r:
                body += "<td>%s</td>" % c
            body += "</tr>"
    body += '</table>'
    return body


def get_observers():
    observers = dict()
    work_book = xlrd.open_workbook(mail_path, encoding_override="utf-8")
    sheet = work_book.sheets()[SHEET_POSITION]
    for row_index in range(sheet.nrows):
        if row_index <= HEADER_OFFSET:
            continue
        observers.update({sheet.row_values(row_index)[0].strip(): sheet.row_values(row_index)[1].strip()})
    return observers


def send_mail(**kwargs):
    receiver = kwargs.get('receiver')
    host = kwargs.get('host')
    port = kwargs.get('port')
    pwd = kwargs.get('pwd')
    body = kwargs.get('body')
    sender = kwargs.get('sender')

    msg = MIMEText(body, 'html', 'utf-8')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = SUBJECT  # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    s.login(sender, pwd)  # 登陆邮箱
    s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！


if __name__ == '__main__':
    import os
    ignored_list = [u'韩继林']

    root_path = os.path.dirname(os.getcwd())
    meta_path = os.path.join(root_path, u"resource/3月考勤明细 .xls")
    mail_path = os.path.join(root_path, u"resource/邮箱通讯录.xlsx")
    header, data = parser(meta_path)

    groups = group(data)
    publish(header)
