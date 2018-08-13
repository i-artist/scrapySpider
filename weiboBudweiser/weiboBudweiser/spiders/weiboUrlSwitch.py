import hashlib
import json
import time
import re
import scrapy
import redis

from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT
class WeiboPCSearchURLSpider(RedisCrawlSpider):
# class WeiboPCSearchURLSpider(scrapy.Spider):
    name = "weiboUrlSwitchZhong"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']

    start_urls = [
        "https://m.weibo.cn/status/GsqBY7XuI"
    ]
    dr = re.compile(r'<[^>]+>', re.S)
    redis_key = "weiboUrlSwitchSpiderZhong:start_urls"
    REDIS_STORE = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    def parse(self,response):
        jsonData = json.loads(response.text.split("var $render_data = [")[-1].split("][0] || {};")[0])
        M_status = jsonData["status"]
        mid = M_status["mid"]
        retweet = int(M_status["reposts_count"])
        comment = int(M_status["comments_count"])
        likeCount = int(M_status["attitudes_count"])
        #push到主贴详情

        self.REDIS_STORE.lpush("weiboArticleDetailSpiderZhong:start_urls","https://m.weibo.cn/status/{}".format(mid))
        #push到评论信息
        if comment > 0:
            self.REDIS_STORE.lpush("weiboCommentSpiderZhong:start_urls","https://m.weibo.cn/api/comments/show?id={}&page=1".format(mid))
        #push到点赞信息
        if likeCount > 0:
            self.REDIS_STORE.lpush("weiboLikeSpiderZhong:start_urls","https://m.weibo.cn/api/attitudes/show?id={}&page=1".format(mid))
        #push到转发信息
        if retweet > 0:
            self.REDIS_STORE.lpush("weiboRetweetSpiderZhong:start_urls","https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(mid))

