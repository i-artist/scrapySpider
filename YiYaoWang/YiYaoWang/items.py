# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YiyaowangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class YiYaoWangCommentItem(scrapy.Item):
    url = scrapy.Field()
    commentContent = scrapy.Field()
    commentDate = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
            insert into [Test].[dbo].[YiYaoWang]([url],[commentContent],[commentDate])
            values (%s,%s,%s)
        """
        params = (
            self["url"],self["commentContent"],self["commentDate"]
        )

        return insert_sql,params