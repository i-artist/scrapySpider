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
from weiboBudweiser.items import weiboTWLItem,saveUserLookInfo
class weiboArticleDetailSpider(RedisCrawlSpider):
# class weiboCommentSpider(scrapy.Spider):
    name = "weiboCommentSpider"
    allowed_domain = ['m.weibo.cn', 'weibo.com', 's.weibo.com']
    start_urls = [
        "https://m.weibo.cn/api/comments/show?id=4241095770447355&page=1",
        "https://m.weibo.cn/api/comments/show?id=4265401519511724&page=1",
        "https://m.weibo.cn/api/comments/show?id=4248605139226549&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4254387528044384&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4252994427869312&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4249806102383320&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4253744085036725&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4254746754127222&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4247158562020287&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4266738159896049&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4249635273557359&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4267784722513800&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4249635297803932&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4265463321566611&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4264008766816450&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4264148294487646&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4262512981905510&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4263963514563020&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4263239640994866&page=1",
        # "https://m.weibo.cn/api/comments/show?id=4265971839206063&page=1"
    ]
    redis_key = "weiboCommentSpiderZhong:start_urls"
    def parse(self,response):
        jsonData = json.loads(response.text)
        TweetID = response.url.split("id=")[-1].split("&page")[0]
        current_page = response.url.split("page=")[-1]
        if jsonData["msg"] == "数据获取成功":
            item = weiboTWLItem()
            try:
                for comment in jsonData["data"]["hot_data"]:
                    item["TweetID"] = TweetID
                    item["UserID"] = comment["user"]["id"]
                    item["UserName"] = comment["user"]["screen_name"]
                    item["Content"] = comment["text"]
                    item["PostTime"] = self.is_valid_date(comment['created_at']) + ' '
                    item["via"] = "comment"
                    item["pid"] = comment["id"]
                    item["like"] = comment['like_counts']

                    yield item
            except:
                for comment in jsonData["data"]["data"]:
                    try:
                        item["TweetID"] = TweetID
                        item["UserID"] = comment["user"]["id"]
                        item["UserName"] = comment["user"]["screen_name"]
                        item["Content"] = comment["text"]
                        item["PostTime"] = self.is_valid_date(comment['created_at']) + ' ' + '00:00:00'
                        item["via"] = "comment"
                        item["pid"] = comment["id"]
                        item["like"] = comment['like_counts']
                    except:
                        print("error")

                    yield item
            current_page = int(current_page) + 1
            yield scrapy.Request("https://m.weibo.cn/api/comments/show?id={}&page={}".format(TweetID, current_page),
                          callback=self.parse,  dont_filter=False)


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