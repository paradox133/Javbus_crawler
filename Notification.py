#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
sender = 'paradox133119@gmail.com'
receivers = ['paradox133119@gmail.com']  
from_addr = 'paradox1331191@gmail.com'
password = 'kdidsedyzvvynfmn'
smtp_server='smtp.gmail.com'


def send_notification(subject,body):
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    body='Python script automatic result\n'+body
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header("robot", 'utf-8')   # 发送者
    message['To'] =  Header("user", 'utf-8')        # 接收者

    # subject = 'Python SMTP Email Test'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP_SSL(smtp_server,465)
        smtpObj.set_debuglevel(1)
        smtpObj.login(from_addr, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Successful")
    except smtplib.SMTPException:
        print("Error: cannot send")