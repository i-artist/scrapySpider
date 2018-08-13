# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



from twisted.enterprise import adbapi
import pymssql

class Yi(object):
    def process_item(self, item, spider):
        return item

class YiYaoWangPipelines(object):
    def __init__(self):
        dbparams = dict(
            host = "123.56.196.177",
            # database = "SinaWeiboApi",
            user = "shengen.zhong",
            password = "zhong0000@"
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