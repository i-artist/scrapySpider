import json
import redis
import hashlib
import scrapy
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from weiboBudweiser.settings import REDIS_HOST,REDIS_PORT
class weiboUserArticle(RedisCrawlSpider):
# class weiboUserArticle(scrapy.Spider):
    name = "weiboArticleListSpider"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']
    start_urls = [
        "https://m.weibo.cn/api/container/getIndex?containerid=2304131191258655&page=1",
        "https://m.weibo.cn/api/container/getIndex?containerid=2304131373381810&page=1"
    ]

    redis_key = "weiboPersonTweetAllSpiderZhong:start_urls"
    REDIS_STORE = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    def parse(self,response):
        weiboJsonData = json.loads(response.text)
        cards = weiboJsonData["data"]["cards"]
        try:
            if cards[0]["name"] == "暂无微博":
                pass
        except:
            currentPage = response.url.split("&page=")[-1]
            spiderUrl = response.url.split("&page=")[0]
            for card in cards:
                mid = card["mblog"]["mid"]
                likeCount = card["mblog"]["attitudes_count"]
                retweet = card["mblog"]["reposts_count"]
                comment = card["mblog"]["comments_count"]
                startUrl = "https://m.weibo.cn/status/%s?colourdataid=C101320" % (mid)
                hashMD5 = hashlib.md5()
                hashMD5.update(startUrl.encode(encoding='utf-8'))
                R_status = self.REDIS_STORE.sadd("weiboArticleHashTestZZqqw:dupefilter",hashMD5.hexdigest())
                if 1 == 1:
                    self.REDIS_STORE.lpush("weiboArticleDetailSpiderZhong:start_urls",
                                                "https://m.weibo.cn/status/%s?colourdataid=C101320" % (mid))
                    if comment > 0:
                        self.REDIS_STORE.lpush("weiboCommentSpiderZhong:start_urls",
                                               "https://m.weibo.cn/api/comments/show?id={}&page=1".format(mid))
                    if likeCount > 0:
                        self.REDIS_STORE.lpush("weiboLikeSpiderZhong:start_urls",
                                               "https://m.weibo.cn/api/attitudes/show?id={}&page=1".format(mid))
                    if retweet > 0:
                        self.REDIS_STORE.lpush("weiboRetweetSpiderZhong:start_urls",
                                               "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(
                                                   mid))

                else:
                    print("url重复")
            NewPage = int(currentPage) + 1
            if NewPage < 6 :

                NewUrl =  "{}&page={}".format(spiderUrl,NewPage)
                yield scrapy.Request(url=NewUrl,callback=self.parse,dont_filter=True)