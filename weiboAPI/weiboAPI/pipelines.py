# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import pymssql
class WeiboapiPipeline(object):
    def process_item(self, item, spider):
        return item


class weiboInsertSqlPipelines(object):
    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host = settings["SQL_HOST"],
            database = settings["SQL_DBNAME"],
            user = settings["SQL_USER"],
            password = settings["SQL_PASSWD"]
        )

        dbpool = adbapi.ConnectionPool("pymssql",**dbargs)
        return cls(dbpool)
    def __init__(self,dbpool):
        self.dbpool = dbpool

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql,params)