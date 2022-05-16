# -*- coding:utf-8 -*-
# Author: 张来吃
# Version: 1.0
# Contact: laciechang@163.com

# -----------------------------------------------------
# 请注意：该脚本仅可在达芬奇17及以上版本内部运行
# 请先确保下方涉及的库可用
# -----------------------------------------------------

import json
import requests
import math
import time
import hmac
import hashlib
import base64
import urllib.parse

# ---------------------------------------------------------------

# 请在下方填写你的钉钉机器人信息，注意保留引号

sec_code = "***" # 通常为SEC开头的一串代码
webhook_url = "***" # 通常为https开头的一个url地址

# ---------------------------------------------------------------

def send_dd(content, title):
    sign = "&timestamp={0}&sign={1}".format(sec()[0], sec()[1])
    webhook = webhook_url
    url = webhook + sign
    header = {"Content-Type":"application/json"}
    data = {"msgtype":"markdown",  "markdown":{"title": "%s" % title,"text":"%s" % content},  
        "at":{  "atMobiles":[], 
        "isAtAll": False  
        }
    } 
    sendData = json.dumps(data)
    response = requests.request("POST", url, data=sendData, headers=header)

def sec():
    timestamp = str(round(time.time() * 1000))
    secret = sec_code
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

def getJobDetailsBasedOnId(project, jobId):
    jobList = project.GetRenderJobList()
    for jobDetail in jobList:
        if jobDetail["JobId"] == jobId:
            return jobDetail
    return ""

def reformatJobDetail(detail):
    o = "- 任务名称：{0}\n".format(str(detail['RenderJobName']))
    o += "- 输出路径：{0}\n".format(str(detail['TargetDir']))
    o += "- 文件名：{0}\n".format(str(detail['OutputFilename']))
    o += "- 输出分辨率：{0}x{1}\n".format(str(detail['FormatWidth']), str(detail['FormatHeight']))
    return o

def reformatJobStatus(status):
    time = int(math.floor(int(status['TimeTakenToRenderInMs'])/1000))

    o = "- 当前状态：{0}\n".format(str(status['JobStatus']))
    o += "- 完成比例：{0}%\n".format(str(status['CompletionPercentage']))
    o += "- 耗时：{0}时{1}分{2}秒\n".format(int(math.floor(time/3600)), int(math.floor(time/60)), time)
    return o

def main():
    project = bmd.scriptapp('Resolve').GetProjectManager().GetCurrentProject()
    project_name = project.GetName()
    detailstatus = project.GetRenderJobStatus(job)

    title = "\"{0}\"的渲染报告: {1}".format(project_name, status)
    content = ""

    if len(str(error)) >= 1:
        content += "## 错误信息: \n\"{0}\"\n".format(error)

    content += "## 执行情况:\n{0}\n".format(reformatJobStatus(detailstatus))
    content += "## 任务细节: \n{0}".format(reformatJobDetail(getJobDetailsBasedOnId(project, job)))
    
    send_dd(content, title)

if __name__ == '__main__':
    main()