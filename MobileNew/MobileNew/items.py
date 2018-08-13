# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose ,TakeFirst, Join


class MobilenewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CreateTime = scrapy.Field()
    Brand = scrapy.Field()
    Model = scrapy.Field()
    IssueDate = scrapy.Field()
    System = scrapy.Field()
    Keyboard = scrapy.Field()
    NetWorkType = scrapy.Field()
    Camera = scrapy.Field()
    MobileDesign = scrapy.Field()
    ScreenSize = scrapy.Field()
    Url = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into [DC_MobileProduct].[dbo].[BasicInfoTransform] ([Model],[Brand],[IssueDate],[操作系统],
            [2G/3G/4G电话],[拍照功能],[手机设计],[键盘],[屏幕尺寸],[URL])
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            str(self["Model"]),str(self["Brand"]),str(self["IssueDate"]),str(self["System"]),str(self["NetWorkType"]),
            str(self["Camera"]),str(self["MobileDesign"]),str(self["Keyboard"]),str(self["ScreenSize"]),str(self["Url"])
        )
        return insert_sql,params

class MobileItemLoader(ItemLoader):
    default_output_processor = TakeFirst()