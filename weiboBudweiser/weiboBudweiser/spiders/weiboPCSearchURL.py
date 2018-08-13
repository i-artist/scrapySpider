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
    name = "weiboPCSearchURL"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']

    start_urls = [
        "https://s.weibo.com/weibo/%25E8%258F%25A0%25E8%2590%259D%25E5%2595%25A4&region=custom:41:1000&typeall=1&suball=1&timescope=custom:2018-07-16-0:2018-07-25-0&page=1",
        "https://s.weibo.com/weibo/%25E8%258F%25A0%25E8%2590%259D%25E5%2595%25A4&typeall=1&suball=1&timescope=custom:2018-07-11-0:2018-07-25-0&region=custom:41:1000&page=1"
    ]
    dr = re.compile(r'<[^>]+>', re.S)

    REDIS_STORE = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    def parse(self,response):
        SearchBrand = ""
        try:
            SearchBrand = re.findall(r'.*?weibo/(.*?)&', response.url)[0]
        except:
            SearchBrand = ""
        urlQuery = response.url.split("&")[1:]
        region,startTime,endTime = '','',''
        for param in urlQuery:
            pts = param.split("=")
            if(pts[0] == 'region'):
                region = pts[1]
            if(pts[0] == 'timescope'):
                startTime = pts[1].split(":")[1]
                endTime = pts[1].split(":")[2]
        for list in response.css("script"):
            if "{\"pid\":\"pl_weibo_direct\"" in str(self.dr.sub('', list.extract())):
                htmlData = json.loads(list.extract().replace('<script>STK && STK.pageletM && STK.pageletM.view(','').replace(')</script>',''))
                soup = BeautifulSoup(htmlData["html"],'lxml')
                midsDOM = soup.select("div[action-type=\"feed_list_item\"]")

                for item in midsDOM:
                    mid = item.attrs["mid"]
                    startUrl = "https://m.weibo.cn/status/%s?startTime=%s&endTime=%s&SearchBrand=%s" %(mid,startTime,endTime,SearchBrand)
                    hashMD5 = hashlib.md5()
                    hashMD5.update(startUrl.encode(encoding='utf-8'))
                    # status = self.REDIS_STORE.sadd("")



