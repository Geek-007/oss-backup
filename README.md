# oss-backup
### 1. 环境说明

* python 版本 : 3.0+ 
* Python 依赖 : oss2
* 系  统  平  台: linux 

### 2. 使用描述
编辑**backupToOSS.py**文件，替换掉下面的字符串

```bash
# OSS相关验证信息
auth = oss2.Auth('<KEY>','<SECRET>')
endpoint = '<ENDPOINT>'
bucket = oss2.Bucket(auth, endpoint, '<BUCKET>')

# 企业微信相关信息
corpid = '<CORPID>'
agentId = <AGENGID>
corpsecret = '<CORP_SECRET>'
```

修改完成后，使用该脚本并传递参数

```bash
# 参数1: 需要备份的文件路径
# 参数2: 远端的目录, 不能以'/'作为开头和结尾
# 例:
python backupToOSS.py /data/backup/something.log 2018/08/21/log
```

