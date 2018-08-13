# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HaodfspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class HaodfKeywordDetailItem(scrapy.Item):
    grade = scrapy.Field() #职位
    hospitalForArticle = scrapy.Field() #医院
    doctorId = scrapy.Field() #id
    doctorName = scrapy.Field() #name
    articleId = scrapy.Field()
    postTime = scrapy.Field()
    pageView = scrapy.Field()
    articleContent = scrapy.Field()
    comment = scrapy.Field()
    keyword = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into [Test].[dbo].[haodf] ([grade],[hospitalForArticle],[doctorId],[doctorName],[articleId],
            [postTime],[pageView],[articleContent],[comment],[keyword])
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        params = (str(self["grade"]),str(self["hospitalForArticle"]),str(self["doctorId"]),str(self["doctorName"]),
                  str(self["articleId"]),str(self["postTime"]),str(self["pageView"]),str(self["articleContent"]),
                  str(self["comment"]),str(self["keyword"]))

        return insert_sql,params
