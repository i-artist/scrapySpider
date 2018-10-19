import json
import redis
import scrapy
import datetime
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider
from weiboAPI.items import weiboUserTagItem

class weiboUserTagSpider(scrapy.Spider):
    name = "weiboUserTagSpider"
    allowed_domain = ["weibo.com"]
    start_urls = [
        "https://c.api.weibo.com/2/tags/tags_batch/other.json?access_token=xxxxxx&uids=1645599505,5992829552,3032262772,2975270515"
    ]

    def parse(self,response):
        tagsArray = json.loads(response.text)
        for user_tag in tagsArray:
            tag_item = weiboUserTagItem()
            tag_item["userID"] = str(user_tag["id"])
            lables = []
            for lable_obj in user_tag["tags"]:
                for lable in lable_obj:
                    if (lable != "weight" and lable != "flag"):
                        lables.append(lable_obj[lable])
            tag_item["lables"] = str(lables)
            yield tag_item