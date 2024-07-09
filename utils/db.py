#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-16  17:33
# @Author  : heshuai.huang
# @Desc:
import pymysql

# 连接数据库的配置信息，请根据实际情况替换
db_config = {
    'host': '127.0.0.1',
    'user': 'crawl',
    'password': 'H46O7Y1xUz7W2VYafJkV',
    'db': 'crawler_db',
    'charset': 'utf8mb4'
}

# 假设这是你的爬虫获取的数据
data_to_insert = [
    {"req_id": 1, "resp_id": 2, "query": "example query", "content": "example content"},
    # 可以添加更多数据...
]


def insert_into_mysql(data):
    try:
        # 连接到MySQL数据库
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # SQL 插入语句
            # sql = "INSERT INTO crawl_enterprise_kimi (req_id, resp_id, query, content) VALUES (%s, %s, %s, %s)"
            sql = """
            INSERT INTO crawl_enterprise_kimi (req_id, resp_id, query, content) 
            VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
                req_id = VALUES(req_id),
                resp_id = VALUES(resp_id), 
                query = VALUES(query), 
                content = VALUES(content)
            """

            # 执行批量插入
            for item in data:
                cursor.execute(sql, (item["req_id"], item["resp_id"], item["query"], item["content"]))

            # 提交事务
            connection.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if connection:
            connection.close()


# 调用函数，将数据插入数据库
insert_into_mysql(data_to_insert)

print("Data inserted successfully.")