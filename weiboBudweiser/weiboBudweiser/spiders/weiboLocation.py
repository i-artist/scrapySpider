import re
import json
import time
import redis
import scrapy
import datetime
from dateutil import parser
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT
from weiboBudweiser.items import weiboLocationInfoItem
class weiboLocationInfo(RedisCrawlSpider):
# class weiboLocationInfo(scrapy.Spider):
    name = "weiboLocationInfo"
    allowed_domain = ['m.weibo.cn']
    start_urls = [
        "https://m.weibo.cn/api/container/getIndex?containerid=2302831000099042_-_INFO",
    ]
    redis_key = "weibofansInfozzz:start_urls"
    def parse(self,response):
       jsonData = json.loads(response.text)["data"]["cards"]
       info_item = weiboLocationInfoItem()
       a = response.url.split("=230283")[-1]
       b = a.split("_-_")[0]
       info_item["uid"] = b
       info_item["location"] = " "
       info_item["birthday"] = " "
       try:
           for card in jsonData:
               try:
                   for list in card["card_group"]:
                        try:
                            if "所在地" == list["item_name"]:
                                info_item["location"] = list["item_content"]
                                print(list["item_content"])
                            if "生日" == list["item_name"]:
                                info_item["birthday"] = list["item_content"]
                                print(list["item_content"])
                            if "性别" == list["item_name"]:
                                info_item["gender"] = list["item_content"]
                        except Exception as e:
                            print(e)
               except Exception as E:
                   print('e',E)
           yield info_item


       except Exception as a:
           print(a)
