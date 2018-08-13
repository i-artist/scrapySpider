# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymssql
from twisted.enterprise import adbapi
#
# class MobilenewPipeline(object):
#     def process_item(self, item, spider):
#         return item
#
#
# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(host="qdm168866545.my3w.com" ,port=3306,user="qdm168866545",password="********",database="qdm168866545_db" , charset='utf8')
#         self.cursor = self.conn.cursor()
#
#     def process_item(self,item,spider):
#         insert_sql = """
#             insert into Mobile(CreateTime,Brand,Model,IssueDate,System,Keyboard,NetWorkType,Camera,MobileDesign,ScreenSize,Url)
#             values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')
#         """ % (item["CreateTime"],item["Brand"],item["Model"],item["IssueDate"],item["System"],item["Keyboard"],item["NetWorkType"],item["Camera"],item["MobileDesign"],item["ScreenSize"],item["Url"])
#         print(insert_sql)
#         self.cursor.execute(insert_sql)
#     pass
#

class MysqlPipeline(object):
    def __init__(self):
        dbparams = dict(
            host = "123.57.176.134",
            # database = "DC_XCAR_BBS",
            user = "shenen.zhong",
            password = "*******"
        )

        self.dbpool = adbapi.ConnectionPool("pymssql",**dbparams)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql,params)
