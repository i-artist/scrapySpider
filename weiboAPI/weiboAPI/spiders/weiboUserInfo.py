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
class weiboUserInfoSpider(scrapy.Spider):
    name = "weiboUserInfoSpider"
    allowed_domain = ["weibo.com"]
    start_urls = [
        "https://c.api.weibo.com/2/users/show_batch/other.json?access_token=xxxxxxxxxxxxx&uids=1811626164,1827889057,1727661660,1411489797,5559148481,1834982335,1390365835,1667087750,2429077634,2440415545,1835976975,2491528833,1818271840,1728041302,1768006845,1249458720,1463354504,5399384357,2801288777,5653982271,1389595163,6175832951,1782540861,2492566240,3533840185,5416809835,2694793283,5847475496,1760938994,2054880800,1278523234,2196062723,1086781301,3027753170,3052592005,1648371701,1768346942,1640799014,2504952427,1716363362",

        ]
    redis_key = "abcABC:start_urls"

    def parse(self,response):
        Users = json.loads(response.text)["users"]
        for user in Users:
            user_item = WeiboUserInfoItem()
            user_item['userID'] = str(user["id"])
            user_item['screen_name'] = user["screen_name"]
            user_item['Location'] = user["location"]
            user_item['Description'] = user["description"]
            user_item['url'] = "https://weibo.com/u/"+user["idstr"]
            user_item['profile_image_url'] = user["profile_image_url"]
            user_item['gender'] = user["gender"]
            user_item['followers_count'] = user["followers_count"] #粉丝数
            user_item['friends_count'] = user["friends_count"]     #关注数
            user_item['statuses_count'] = user["statuses_count"]   #微博数
            user_item['verified'] = user["verified"]
            user_item['verified_type'] = user["verified_type"]
            yield user_item

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