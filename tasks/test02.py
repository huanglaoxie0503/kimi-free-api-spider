#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-15  10:31
# @Author  : heshuai.huang
# @Desc:
import requests
import json


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNTc0MDk3MCwiaWF0IjoxNzE1NzQwMDcwLCJqdGkiOiJjcDIxcjloa3FxNHBkcmRobmw4MCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNwMWdzc2o1Y2Z1a2VwMnU3bGQwIiwic3BhY2VfaWQiOiJjcDFnc3NqNWNmdWtlcDJ1N2xjZyIsImFic3RyYWN0X3VzZXJfaWQiOiJjcDFnc3NqNWNmdWtlcDJ1N2xjMCJ9.MRLSfb8r-OwsuYbRDzWHvLpBo-Gc_xDcY5s5JQpxAQV_wl9cgMrU2V2tsdQBeUAU8IDaC4GE88UTtDQiySavqw",
    "content-type": "application/json",
    "origin": "https://kimi.moonshot.cn",
    "priority": "u=1, i",
    "r-timezone": "Asia/Shanghai",
    "referer": "https://kimi.moonshot.cn/chat/cp21kh2lnl9ebq63v1q0",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-traffic-id": "cp1gssj5cfukep2u7ld0"
}
cookies = {
    "_ga": "GA1.1.332909179.1715670617",
    "_gcl_au": "1.1.943713966.1715670617",
    "_ga_Z0ZTEN03PZ": "GS1.1.1715675852.3.1.1715675855.0.0.0",
    "Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b": "1715670617,1715739135",
    "Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b": "1715739135",
    "_ga_YXD8W70SZP": "GS1.1.1715739134.2.1.1715739250.0.0.0"
}
url = "https://kimi.moonshot.cn/api/chat/cp21kh2lnl9ebq63v1q0/segment/scroll"
data = {
    "segment_ids": [
        "cp21no9kqq4l30icest0",
        "cp21no9kqq4l30icestg"
    ]
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)
response.encoding = 'utf-8'

print(response.text)