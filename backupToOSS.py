#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : backupToOSS.py
# @Author: Lyon Dong
# @Date  : 2018/6/22
# @Email  : i@dongliwu.com

# 参数说明:
#    参数1: 需要备份的文件路径
#    参数2: 远端的目录, 不能以'/'作为开头和结尾

import os
import sys
import time
import oss2
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from tools import weChatMsg

# OSS相关验证信息
auth = oss2.Auth('<KEY>','<SECRET>')
endpoint = '<ENDPOINT>'
bucket = oss2.Bucket(auth, endpoint, '<BUCKET>')

# 企业微信相关信息
corpid = '<CORPID>'
agentId = <AGENGID>
corpsecret = '<CORP_SECRET>'
url = 'https://qyapi.weixin.qq.com'


if len(sys.argv) !=  3:
    print("参数不正确!")
    exit(1)

# 获取备份文件名
if os.path.exists(sys.argv[1]):
    filename = sys.argv[1]
else:
    print("文件不存在!")
    exit(1)

# 远端备份文件名
dirname = sys.argv[2]
remote_filename = dirname + '/' + os.path.basename(filename)

# 开始分片
total_size = os.path.getsize(filename)
part_size = determine_part_size(total_size, preferred_size=100 * 1024)

# 初始化分片
upload_id = bucket.init_multipart_upload(remote_filename).upload_id
parts = []

# 逐个上传分片
with open(filename, 'rb') as fileobj:
    part_number = 1
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        result = bucket.upload_part(remote_filename, upload_id, part_number,SizedFileAdapter(fileobj, num_to_upload))
        parts.append(PartInfo(part_number, result.etag))

        offset += num_to_upload
        part_number += 1

# 完成分片上传
result = bucket.complete_multipart_upload(remote_filename, upload_id, parts)


# CRC64验证
def calculate_file_crc64(file_name, block_size=1024 * 1024, init_crc=0):
    """计算文件的CRC64
    :param file_name: 文件名
    :param block_size: 计算CRC64的数据块大小，默认1024KB
    :return 文件内容的CRC64值
    """
    with open(file_name, 'rb') as f:
        crc64 = oss2.utils.Crc64(init_crc)
        while True:
            data = f.read(block_size)
            if not data:
                break
            crc64.update(data)

    return crc64.crc

crc64 = calculate_file_crc64(filename)

# 构建推送信息
def messages(status):
    """
    :param status: 备份成功或失败
    :return: 推送的信息
    """
    hostname = os.popen('hostname').read()
    values = '主机名:'  + hostname + '备份状态:' + status + '\n' + '备份文件: ' + filename + '\n' + '备份时间: ' + time.strftime("%Y-%m-%d %H:%M:%S")
    return values

if(str(crc64) == result.headers['x-oss-hash-crc64ecma']):
    os.remove(filename)
    msg = messages('成功')
else:
    msg = messages('失败')

# 发送微信通知
weChatMsg.notify(url, corpid, corpsecret, agentId, msg)