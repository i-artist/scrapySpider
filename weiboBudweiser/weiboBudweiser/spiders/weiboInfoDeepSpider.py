import re
import json
import redis
import scrapy
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider
from weiboBudweiser.items import weiboUserInfoDeepItem
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT

class weiboInfoSpider(RedisCrawlSpider):
# class weiboInfoSpider(scrapy.Spider):
    name = "weiboInfoDeepSpider"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']

    start_urls = [
        "https://m.weibo.cn/profile/info?uid=6518484674",
        # "https://m.weibo.cn/profile/info?uid=1752101967"
    ]
    dr = re.compile(r'<[^>]+>', re.S)
    redis_key = "weiboPersonInfoSpiderZhong:start_urls"
    REDIS_STORE = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    def parse(self,response):
        if "微博-出错了" in response.text:
            print("错误ID")
        else:
            status = response.text
            userData = json.loads(status)
            if userData["ok"] == 1 :
                userInfoItem = {}
                userJson = userData["data"]["user"]
                userInfoItem["screen_name"] = userJson["screen_name"]
                userInfoItem["followers_count"] = userJson["followers_count"]
                userInfoItem["follow_count"] = userJson["follow_count"]
                userInfoItem["verified"] = userJson["verified"]
                userInfoItem["verified_type"] = userJson["verified_type"]
                userInfoItem["uid"] = userJson["id"]
                userInfoItem["gender"] = userJson["gender"]
                yield scrapy.Request("https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO".format(userJson["id"]),callback=self.deepParse,meta=userInfoItem)
    def deepParse(self,response):
       infoData = response.meta
       jsonData = json.loads(response.text)["data"]["cards"]
       info_item = weiboUserInfoDeepItem()
       a = response.url.split("=230283")[-1]
       b = a.split("_-_")[0]
       info_item["fansID"] = b
       info_item["location"] = ""
       info_item["birthday"] = ""
       info_item["screen_name"] = infoData["screen_name"]
       info_item["followers_count"] = infoData["followers_count"]
       info_item["follow_count"] = infoData["follow_count"]
       info_item["verified"] = infoData["verified"]
       info_item["verified_type"] = infoData["verified_type"]
       info_item["gender"] = infoData["gender"]
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
                        except Exception as e:
                            print(e)
               except Exception as E:
                   print('e',E)
           yield info_item


       except Exception as a:
           print(a)

