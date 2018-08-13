import hashlib
import json
import time
import re
import scrapy
import redis
import requests
from lxml import etree
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT

class WeiboPCSearchURLSpider(scrapy.Spider):
    name = "weiboUserFansPC"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']

    start_urls = [
        "https://weibo.com/1744768687/fans?pids=Pl_Official_RelationFans__67&cfs=600&relate=fans&t=1&f=1&type=&ajaxpagelet=1&ajaxpagelet_v6=1&ref=/1744768687/fans&_t=FM_153389091804427&Pl_Official_RelationFans__67_page=2"
    ]
    dr = re.compile(r'<[^>]+>', re.S)

    REDIS_STORE = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def parse(self, response):
        fansData = response.text.split("parent.FM.view(")[-1].split(")</scrip")[0]
        json_data = json.loads(fansData)
        soup = BeautifulSoup(json_data["html"],'lxml')
        action_data = soup.select("dt[class=\"mod_pic\"] a")
        fansID = []
        for tag in action_data:
            select_PC = tag.attrs["href"]
            b= select_PC[:3]
            if select_PC[:3] == "/u/":
                fansID.append(select_PC[3:13])
            else:
                fansID.append(select_PC[1:11])

        print(fansID)
        currentPage = response.url.split("Pl_Official_RelationFans__67_page=")[-1]
        currentUrl = response.url.split("Pl_Official_RelationFans__67_page=")[0]
        currentPage = int(currentPage) + 1
        yield scrapy.Request(url = "{}Pl_Official_RelationFans__67_page={}".format(currentUrl,currentPage),callback=self.parse)
