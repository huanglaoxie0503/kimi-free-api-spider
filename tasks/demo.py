#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-14  15:23
# @Author  : heshuai.huang
# @Desc:
import requests
import json
from loguru import logger

from utils import extract_first_column_values

headers_token = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzU0MDM3OCwiaWF0IjoxNzE1NzY0Mzc4LCJqdGkiOiJjcDI3cDZpbG5sOTMwbmliamhoZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbm1qdjg4bnNtbWg4M2tmMDg3MCIsInNwYWNlX2lkIjoiY25tanY4OG5zbW1oODNrZjA4NmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY25tanY4OG5zbW1oODNrZjA4NjAifQ.MrHaEMGmMzxQOVSjwfqpYoM1RFJYJpVKinGFnsoIRwkXV19260eKuCV1LyyfK5PBmdCgT7qWfWR6xtyyiVoqZA",
    "priority": "u=1, i",
    "referer": "https://kimi.moonshot.cn/chat/cp27tu4ubms6ha9ht4bg?data_source=tracer&utm_campaign=TR_PbzLg2eV&utm_content=&utm_medium=%E5%BE%AE%E8%BD%AFbing&utm_source=bing&utm_term=&msclkid=2e60aeb707df10abbb9ec8f34833ab6c",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
     "content-type": "application/json",
    "origin": "https://kimi.moonshot.cn",
    "priority": "u=1, i",
    "r-timezone": "Asia/Shanghai",
    # "referer": "https://kimi.moonshot.cn/chat/cp27tu4ubms6ha9ht4bg?data_source=tracer&utm_campaign=TR_PbzLg2eV&utm_content=&utm_medium=%E5%BE%AE%E8%BD%AFbing&utm_source=bing&utm_term=&msclkid=2e60aeb707df10abbb9ec8f34833ab6c",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-traffic-id": "cnmjv88nsmmh83kf0870"
}
cookies = {
    "_ga": "GA1.1.332909179.1715670617",
    "_gcl_au": "1.1.943713966.1715670617",
    "Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b": "1715670617,1715739135",
    "_tea_utm_cache_20001731": "{%22utm_source%22:%22bing%22%2C%22utm_medium%22:%22%E5%BE%AE%E8%BD%AFbing%22%2C%22utm_campaign%22:%22TR_PbzLg2eV%22}",
    "_clck": "zmsqbw%7C2%7Cfls%7C0%7C1596",
    "Hm_lvt_4532beacc312859e0aa3e4a80566b706": "1715753041",
    "Hm_lpvt_4532beacc312859e0aa3e4a80566b706": "1715753041",
    "_ga_31QPQG2YYD": "GS1.1.1715753041.1.0.1715753048.0.0.0",
    "_ga_Z0ZTEN03PZ": "GS1.1.1715752945.4.1.1715753269.0.0.0",
    "Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b": "1715764917",
    "_clsk": "njxmqj%7C1715764985154%7C5%7C0%7Cr.clarity.ms%2Fcollect",
    "_ga_YXD8W70SZP": "GS1.1.1715764023.6.1.1715764985.0.0.0"
}


def get_refresh():
    url = "https://kimi.moonshot.cn/api/auth/token/refresh"
    response = requests.get(url, headers=headers_token, cookies=cookies)
    response.encoding = 'utf-8'
    return response.json()


if __name__ == '__main__':
    url_stream = "https://kimi.moonshot.cn/api/chat/cp27tu4ubms6ha9ht4bg/completion/stream"
    company_values_1 = [
        "小米", "贵州茅台", "理想汽车", "华为"
    ]
    file_path = r'D:\projects\moonshot\195762142490942_1.csv'
    company_values = extract_first_column_values(file_path)
    nums = len(company_values)
    token = get_refresh()
    access_token = token['access_token']
    i = 0
    for company_name in company_values_1:
        i = i + 1
        logger.info(f'共{nums}家公司，正在运行第：{i}家，公司名称：{company_name}')
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": f"{company_name}公司的主营业务"
                }
            ],
            "refs": [],
            "use_search": True,
            "kimiplus_id": "kimi"
        }
        data = json.dumps(data, separators=(',', ':'))
        headers['authorization'] = 'Bearer ' + access_token
        response = requests.post(url_stream, headers=headers, cookies=cookies, data=data)
        response.encoding = 'utf-8'
        stream = response.text
        rows = stream.split('data:')
        ids = []
        for row in rows:
            if not row:
                continue
            try:
                data = json.loads(row)
                event = data.get('event')
                if event in ('req', 'resp'):
                    ids.append(data['id'])
            except Exception as e:
                print(e)
        print(ids)

        url_scroll = "https://kimi.moonshot.cn/api/chat/cp27tu4ubms6ha9ht4bg/segment/scroll"
        data = {
            "segment_ids": ids
        }
        data = json.dumps(data, separators=(',', ':'))
        response_1 = requests.post(url_scroll, headers=headers, cookies=cookies, data=data)

        content = response_1.text
        print(content)
