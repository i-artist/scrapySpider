import re
import json
import time
import redis
import scrapy
import datetime
import scrapy_redis
from dateutil import parser
from scrapy_redis.spiders import RedisCrawlSpider
from weiboAPI.items import WeiboUserInfoItem
class weiboUserFansInfoSpider(scrapy.Spider):
    name = "weiboUserFansInfoSpider"
    allowed_domain = ["weibo.com"]
    start_urls = [
        "https://c.api.weibo.com/2/friendships/followers/biz.json?access_token=2.008CsEuB034XBMaa833a08b39W2uUE"
    ]

    def parse(self, response):
        R_Text = json.loads(response.text)
        for user in R_Text["users"]:
            id = user["id"]
            screen_name = user["screen_name"]
            location = user["location"]
            description = user["description"]
            iconUrl = user["profile_image_url"]
            verified = user["verified"]
            verified_type = user["verified_type"]
            gender = user["gender"]
            followers_count = user["followers_count"]
            friends_count = user["friends_count"]
            verified_reason = user["verified_reason"]
            statuses_count = user["statuses_count"]
            favourites_count = user["favourites_count"]
            url = "https://weibo.com/u/"+user["idstr"]
            created_at = self.is_valid_date(user["created_at"])

        next_cursor = R_Text["next_cursor"]
        if(next_cursor):
            yield scrapy.Request(url = "https://c.api.weibo.com/2/friendships/followers/biz.json?access_token=2.008CsEuB034XBMaa833a08b39W2uUE&cursor_uid={}".format(next_cursor),
                                 callback=self.parse)




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