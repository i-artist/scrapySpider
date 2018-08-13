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
from weiboBudweiser.items import weiboArticleDetailItemLoader,weiboArticleDetailItem
# class weiboArticleDetailSpider(RedisCrawlSpider):
class weiboArticleDetailSpider(scrapy.Spider):
    name = "weiboArticleDetailSpiderZZ"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']
    start_urls = [
        "https://m.weibo.cn/status/4256265766957090",
        "https://m.weibo.cn/status/4264523881773397",
        "https://m.weibo.cn/status/4268847185973417",

    ]
    redis_key = "weiboArticleDetailSpiderZhong:start_urls"
    REDIS_STORE = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    dr = re.compile(r'<[^>]+>', re.S)
    def parse(self,response):
        item_loader = weiboArticleDetailItemLoader(item=weiboArticleDetailItem(),response=response)
        jsonData = json.loads(response.text.split("var $render_data = [")[-1].split("][0] || {};")[0])
        M_status = jsonData["status"]
        item_loader.add_value("userName",M_status["user"]["screen_name"])
        item_loader.add_value("userIcon",M_status["user"]["profile_image_url"])
        item_loader.add_value("tweetId",M_status["mid"])
        item_loader.add_value("userUrl",'http://weibo.com/u/' + str(M_status['user']['id']))
        item_loader.add_value("commentContent",self.dr.sub("",M_status["text"]))
        if(M_status["source"]==""):
            item_loader.add_value("commentDevice"," ")
        else:
            item_loader.add_value("commentDevice", M_status["source"])
        item_loader.add_value("commentTime",self.is_valid_date(str(M_status['created_at'])))
        item_loader.add_value("retweet",M_status["reposts_count"])
        item_loader.add_value("comment",M_status["comments_count"])
        item_loader.add_value("likeCount",M_status["attitudes_count"])
        item_loader.add_value("tweetUrl",'https://weibo.com/' + str(M_status['user']['id']) + '/' + str(M_status['bid']))
        item_loader.add_value("userId",M_status["user"]["id"])
        try:
            tweetPicture = M_status['pics']
            picture = '['
            for pics in tweetPicture:
                picture = picture + pics['url'] + ', '
            picture = picture + ']'
            item_loader.add_value("tweetPicture",picture)
        except Exception as e:
            item_loader.add_value("tweetPicture"," ")
            print("e:", e)

        try:
            item_loader.add_value("orignalUser",M_status['retweeted_status']['user']['screen_name'])
            item_loader.add_value("orignalUserUrl",'https://weibo.com/u/' + str(M_status['retweeted_status']['user']['id']))
            item_loader.add_value("orignalTweetContent",self.dr.sub('', M_status['retweeted_status']['text']))
            item_loader.add_value("orignalRetweet",M_status['retweeted_status']['reposts_count'])
            item_loader.add_value("orignalComment",M_status['retweeted_status']['comments_count'])
            item_loader.add_value("orignalLike",M_status['retweeted_status']['attitudes_count'])
            if(M_status['retweeted_status']['source']==""):
                item_loader.add_value("orignalDevice", "  ")
            else:
                item_loader.add_value("orignalDevice",M_status['retweeted_status']['source'] )
            item_loader.add_value("orignalTweetTime",self.is_valid_date(M_status['retweeted_status']['created_at']))
        except Exception as a:
            item_loader.add_value("orignalUser", " ")
            item_loader.add_value("orignalUserUrl"," ")
            item_loader.add_value("orignalTweetContent"," ")
            item_loader.add_value("orignalRetweet"," ")
            item_loader.add_value("orignalComment"," ")
            item_loader.add_value("orignalLike", " ")
            item_loader.add_value("orignalDevice", " ")
            item_loader.add_value("orignalTweetTime", " ")
        weiboDetail_item = item_loader.load_item()
        yield weiboDetail_item

    def is_valid_date(self, strdate):
        '''''判断是否是一个有效的日期字符串'''
        try:
            if '+0800' in strdate:
                return str(parser.parse(strdate.replace('+0800', '')))
            elif ":" in strdate:
                time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(strdate, "%Y-%m-%d")
            return strdate
        except:
            if '刚刚' in strdate:
                return str(datetime.datetime.now())[0:19]
            elif '小时' in strdate:
                return self.beforeHours2Date(int(re.findall(r'\d+', strdate)[0]))
            elif '昨天' in strdate:
                return str(datetime.date.today() + datetime.timedelta(days=-1)) + strdate.replace('昨天', '')
            elif '分钟' in strdate:
                # return time.strptime('%Y-%m-%d %H:%M:%S',datetime.datetime.now()+ datetime.timedelta(minutes=int('-'+ re.findall(r"\d+\.?\d*",strdate)[0])))
                return str(datetime.datetime.now() + datetime.timedelta(
                    minutes=int('-' + strdate.replace('分钟', '').replace('前', ''))))[0:19]
            elif '秒' in strdate:
                return str(datetime.datetime.now() + datetime.timedelta(
                    seconds=int('-' + strdate.replace('秒', '').replace('前', ''))))[0:19]
            elif '今天' in strdate:
                return str(datetime.date.today()) + strdate.replace('今天', '')
            elif '月' in strdate or '日' in strdate:
                return str(datetime.datetime.now().year) + "-" + strdate.replace('月', '-').replace('日', '')
            else:
                return str(datetime.datetime.now().year) + "-" + strdate

    def beforeHours2Date(self,hours):
        hours = int(hours)
        t = time.time() - hours * 60 * 60
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return t