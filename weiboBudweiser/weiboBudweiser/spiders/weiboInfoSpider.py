import re
import json
import redis
import scrapy
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider
from weiboBudweiser.items import weiboUserInfoItem
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT

class weiboInfoSpider(RedisCrawlSpider):
# class weiboInfoSpider(scrapy.Spider):
    name = "weiboInfoSpider"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']

    start_urls = [
        "https://m.weibo.cn/profile/info?uid=1050577541",
        "https://m.weibo.cn/profile/info?uid=1002805431"
    ]
    dr = re.compile(r'<[^>]+>', re.S)
    redis_key = "weiboUserInfoTable:start_urls"
    REDIS_STORE = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    def parse(self,response):
        if "微博-出错了" in response.text:
            print("错误ID")
        else:
            status = response.text
            userData = json.loads(status)
            if userData["ok"] == 1 :
                userInfoItem = weiboUserInfoItem()
                userJson = userData["data"]["user"]
                userInfoItem["screen_name"] = userJson["screen_name"]
                userInfoItem["followers_count"] = userJson["followers_count"]
                userInfoItem["follow_count"] = userJson["follow_count"]
                userInfoItem["verified"] = userJson["verified"]
                userInfoItem["verified_type"] = userJson["verified_type"]
                userInfoItem["uid"] = userJson["id"]
                userInfoItem["gender"] = userJson["gender"]
                yield userInfoItem


