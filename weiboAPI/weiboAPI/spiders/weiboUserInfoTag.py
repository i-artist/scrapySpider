import re
import json
import time
import redis
import scrapy
from weiboAPI.utils.kafka_push import weiboUserPushKafka
import datetime
import scrapy_redis
from dateutil import parser
from scrapy_redis.spiders import RedisCrawlSpider
class weiboUserInfoSpider(scrapy.Spider):
    name = "weiboUserInfoTagSpider"
    allowed_domain = ["weibo.com"]
    start_urls = [
        "https://c.api.weibo.com/2/users/show_batch/other.json?access_token=xxxxxx&uids=1645599505,5992829552,3032262772,2975270515"
    ]

    def parse(self,response):
        Users = json.loads(response.text)["users"]
        for user in Users:
            user_item = {}
            user_item['userid'] = str(user["id"])
            user_item['username'] = user["screen_name"]
            user_item['location'] = user["location"]
            user_item['introduce'] = user["description"]
            user_item['userUrl'] = "https://weibo.com/u/"+user["idstr"]
            user_item['iconUrl'] = user["profile_image_url"]
            user_item['gender'] = user["gender"]
            user_item['fans'] = user["followers_count"] #粉丝数
            user_item['focus'] = user["friends_count"]     #关注数
            user_item['posts'] = user["statuses_count"]   #微博数
            user_item['verified'] = user["verified"]
            user_item['verifiedtype'] = user["verified_type"]
            user_item["joindate"] = self.is_valid_date(user["created_at"])
            yield scrapy.Request(url = 'https://c.api.weibo.com/2/tags/tags_batch/other.json?access_token=2.00vSFDMH034XBM856918eaf7zwl6kD&uids={}'.format(user_item["userid"]),
                                 callback = self.TagParse,meta = {"KafkaItem":user_item})
    def TagParse(self,response):
        KafkaItem = response.meta["KafkaItem"]
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        KafkaItem["createtime"] = nowTime
        KafkaItem["verifiedreason"] = ""
        KafkaItem["birthday"] = ""
        tagsArray = json.loads(response.text)
        if len(tagsArray) == 0:
            KafkaItem["lable"] = ""
            weiboUserPushKafka("Testweibo_Kafka333").push(KafkaItem)
            print(0)
        else:
            lables = []
            for user_tag in tagsArray:
                tag_item = {}
                for lable_obj in user_tag["tags"]:
                    for lable in lable_obj:
                        if (lable != "weight" and lable != "flag"):
                            lables.append(lable_obj[lable])
                tag_item["lables"] = str(lables)
            KafkaItem["lable"] = lables
            weiboUserPushKafka("Testweibo_Kafka333").push(KafkaItem)
        print(KafkaItem)

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