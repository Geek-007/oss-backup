#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : weChatMsg.py
# @Author: Lyon Dong
# @Date  : 2018/6/22
# @Email  : i@dongliwu.com

import urllib.request
import json

# 发送消息
def notify(url, corpid, corpsecret, agentId, msg):
    # 获取企业微信token
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']

    # 告警内容
    values = {
        "touser": '@all',
        "msgtype": 'text',
        "agentid": agentId,
        "text": {'content': msg},
        "safe": 0
        }
    json_format = bytes(json.dumps(values), 'utf-8')

    send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, token)
    respone = urllib.request.urlopen(urllib.request.Request(url=send_url, data=json_format)).read()
    if_error = json.loads(respone.decode())['errcode']

    return if_error
