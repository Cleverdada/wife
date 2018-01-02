#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText  # 引入smtplib和MIMEText

import xlrd

SHEET_POSITION = 0
HEADER_OFFSET = 1
GROUP_INDEX = 1
SUBJECT = u"2017年11-12月份考勤核对表"

mail_info = dict(
    host='smtp.jszyfz.com',
    port=25,
    sender='zhanglin@jszyfz.com',
    pwd='xhwl20170327'
)

observers = {
    u"张琳": "zhanglin@jszyfz.com",
}


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
    for name, group_data in groups.iteritems():
        observer = observers.get(name)
        if not observer:
            print u"`%s` igored" % name
        else:
            print gen_body(header, group_data)
            mail_info.update({"receiver": observer,
                                "body": gen_body(header, group_data)})
            send_mail(**mail_info)
            print u"`%s`, `%s` send success" % (name, observer)


def gen_body(header, group_data):
    body = u'<h1>12月份考勤，请仔细核对</h1>'
    body +='<table border="1">'
    body += "<tr>"
    for h in header:
        body += "<td><strong>%s</strong></td>" % h
    body += "</tr>"

    for r in group_data:
        body += "<tr>"
        for c in r:
            body += "<td>%s</td>" % c
        body += "</tr>"
    body += '</table>'
    return body


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
    print sender, pwd
    s.login(sender, pwd)  # 登陆邮箱
    s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！


if __name__ == '__main__':
    import os
    root_path = os.path.dirname(os.getcwd())
    header, data = parser(os.path.join(root_path, u"resource/考勤明细_final.xlsx"))
    groups = group(data)
    publish(header)
