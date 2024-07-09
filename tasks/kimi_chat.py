#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-15  10:21
# @Author  : heshuai.huang
# @Desc:
import time
import random
import requests
import json
from loguru import logger
from utils.tools import extract_first_column_values
from utils.db import insert_into_mysql
from settings import REFRESH_TOKEN, ITEMS


def get_headers(token=None):
    base_headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    if token:
        base_headers.update({
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "origin": "https://kimi.moonshot.cn",
            "r-timezone": "Asia/Shanghai",
            "x-traffic-id": "cnmjv88nsmmh83kf0870"
        })
    else:
        base_headers.update({
            "referer": "https://kimi.moonshot.cn/chat/cp27tu4ubms6ha9ht4bg?data_source=tracer&utm_campaign=TR_PbzLg2eV&utm_content=&utm_medium=%E5%BE%AE%E8%BD%AFbing&utm_source=bing&utm_term=&msclkid=2e60aeb707df10abbb9ec8f34833ab6c"
        })
    return base_headers


def get_cookies():
    return {
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


def get_refresh_token():
    url = "https://kimi.moonshot.cn/api/auth/token/refresh"
    token = random.choice(REFRESH_TOKEN)
    logger.warning('当前选择的token：{0}'.format(token))
    response = requests.get(url, headers=get_headers(token=token), cookies=get_cookies())
    response.encoding = 'utf-8'
    return response.json()['access_token']


def get_company_info(company_name, token, chat_id):
    # cp27tu4ubms6ha9ht4bg
    url_stream = f"https://kimi.moonshot.cn/api/chat/{chat_id}/completion/stream"
    data = {
        "messages": [{"role": "user", "content": f"{company_name}公司的介绍、主营业务、主营产品"}],
        "refs": [],
        "use_search": True,
        "kimiplus_id": "kimi"
    }
    headers = get_headers(token)
    response = requests.post(url_stream, headers=headers, cookies=get_cookies(),
                             data=json.dumps(data, separators=(',', ':')))
    response.encoding = 'utf-8'
    return response.text


def parse_stream(stream):
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
            logger.error(e)
    return ids


def scroll_segments(ids, token, chat_id):
    # cp27tu4ubms6ha9ht4bg
    url_scroll = f"https://kimi.moonshot.cn/api/chat/{chat_id}/segment/scroll"
    data = {"segment_ids": ids}
    headers = get_headers(token)
    response = requests.post(url_scroll, headers=headers, cookies=get_cookies(),
                             data=json.dumps(data, separators=(',', ':')))
    return response.text


def get_chat_id(token):
    url = "https://kimi.moonshot.cn/api/chat"
    data = {
        "name": "未命名会话",
        "is_example": False,
        "born_from": "",
        "kimiplus_id": "kimi"
    }
    headers = get_headers(token)
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=get_cookies(), data=data)
    json_data = json.loads(response.text)
    return json_data.get('id')


def main():
    file_path = r'D:\projects\moonshot\195762142490942_1.csv'
    company_values = ITEMS  #extract_first_column_values(file_path)
    # company_values = [
    #     "小米", "贵州茅台", "理想汽车", "华为"
    # ]
    token_info = {
        'access_token': get_refresh_token(),
        'last_refresh_time': time.time(),
        'request_count': 0
    }
    num_companies = len(company_values)
    token = token_info.get('access_token')
    c_id = get_chat_id(token=token)
    for i, company_name in enumerate(company_values, start=1):
        if i < 274:
            continue
        start_time = time.time()
        token = token_info.get('access_token')
        logger.info(f'共{num_companies}家公司，正在运行第：{i}家，公司名称：{company_name}')
        stream = get_company_info(company_name, token, c_id)
        ids = parse_stream(stream)
        logger.info(ids)
        if len(ids) == 0:
            access_token = get_refresh_token()
            new_token_info = {"access_token": access_token}
            # 更新token_info
            token_info.update(new_token_info)
            token_info.update()
            logger.info('更新token：{0}'.format(token_info))
            logger.info(stream)
            continue
        content = scroll_segments(ids, token, c_id)
        content = json.loads(content)
        error = content.get('error')
        error_type = content.get('error_type')
        if error_type or error:
            message = content.get('message') or error.get('message')
            logger.error(message)
            access_token = get_refresh_token()
            new_token_info = {"access_token": access_token}
            # 更新token_info
            token_info.update(new_token_info)
            token_info.update()
            logger.info('更新token：{0}'.format(token_info))
            continue
        items = content.get('items')
        n = len(items)
        rows = []
        if n == 2:
            req_id = items[0].get('id')
            resp_id = items[1].get('id')
            query = items[0].get('content')
            content = items[1].get('content')
            if content is None or len(content) == 0:
                logger.error(items)
                continue
            # data = (req_id, resp_id, query, content)
            row = {
                "req_id": req_id,
                "resp_id": resp_id,
                "query": query,
                "content": content,
            }
            rows.append(row)
        insert_into_mysql(data=rows)
        # for item in items:
        #     id = item.get('id')
        #     text = item.get('content')
        #     if text:
        #         logger.info(text)
        #     else:
        #         error = item.get('error')
        #         message = error.get('message')
        #         logger.error(message)

        end_time = time.time()

        # 计算并打印运行时间
        run_time = end_time - start_time
        print(f"爬虫程序运行时间: {run_time}秒")
        logger.info('---------------------------------&-------------------------------')


if __name__ == '__main__':
    main()
