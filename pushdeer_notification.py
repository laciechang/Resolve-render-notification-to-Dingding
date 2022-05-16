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


# ---------------------------------------------------------------

# 请在下方填写你的PUSHDEER信息，注意保留引号

PUSH_KEY = ["PDU10688T9yhU3mxZYzE6kcs7xHA5fTUBT8KUTl6e"]

# ---------------------------------------------------------------

SERVER = "https://api2.pushdeer.com"
ENDPOINT = "/message/push"

def getJobDetailsBasedOnId(project, jobId):
    jobList = project.GetRenderJobList()
    for jobDetail in jobList:
        if jobDetail["JobId"] == jobId:
            return jobDetail
    return ""

def reformatJobStatus(status):
    time = int(math.floor(int(status['TimeTakenToRenderInMs'])/1000))

    o = "- 当前状态：{0}\n".format(str(status['JobStatus']))
    o += "- 完成比例：{0}%\n".format(str(status['CompletionPercentage']))
    o += "- 耗时：{0}时{1}分{2}秒\n".format(int(math.floor(time/3600)), int(math.floor(time/60)), time)
    return o

def reformatJobDetail(detail):
    o = "- 任务名称：{0}\n".format(str(detail['RenderJobName']))
    o += "- 输出路径：{0}\n".format(str(detail['TargetDir']))
    o += "- 文件名：{0}\n".format(str(detail['OutputFilename']))
    o += "- 输出分辨率：{0}x{1}\n".format(str(detail['FormatWidth']), str(detail['FormatHeight']))
    return o

def send_push_request(title, text, key):
    return requests.get(SERVER + ENDPOINT, params={
        "pushkey": key,
        "text": title,
        "desp": text,
        "type": "markdown"
    }).json()

def push(key):
    project = bmd.scriptapp('Resolve').GetProjectManager().GetCurrentProject()
    timelinename = str(project.GetCurrentTimeline().GetName())
    title = timelinename+'的渲染任务完成了'
    text = ''
    detailstatus = project.GetRenderJobStatus(job)
    text += "## 执行情况:\n{0}\n".format(reformatJobStatus(detailstatus))
    text += "## 任务细节: \n{0}".format(reformatJobDetail(getJobDetailsBasedOnId(project, job)))
    res = send_push_request(title, text, key)
    if res["content"]["result"]:
        result = json.loads(res["content"]["result"][0])
        if result["success"] == "ok":
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    for i in PUSH_KEY:
        push(i)