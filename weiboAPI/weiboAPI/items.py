# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboapiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class weiboUserFansItem(scrapy.Item):
    pass

class WeiboUserInfoItem(scrapy.Item):
    userID = scrapy.Field()
    screen_name = scrapy.Field()
    Location = scrapy.Field()
    Description = scrapy.Field()
    url = scrapy.Field()
    profile_image_url = scrapy.Field()
    gender = scrapy.Field()
    followers_count = scrapy.Field()
    friends_count = scrapy.Field()
    statuess_count = scrapy.Field()
    verified = scrapy.Field()
    verified_type = scrapy.Field()
    statuses_count = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            UPDATE [SinaWeiboAPI].[dbo].[userFansInfoDeep] SET [fansName] = %s,[fans_gender] = %s ,[fansBirthday] = %s,
             [fansVerified] = %s , [fansVerified_type] = %s, [fansLocation] = %s,[fans_followers_count] = %s ,
             [fans_follow_count] = %s, [Description] = %s, [fans_statuses_count] = %s WHERE fansID = %s
        """
        params = (self["screen_name"],self["gender"],str(" "),self["verified"],self["verified_type"],self["Location"],
                  self["followers_count"],self["friends_count"],self["Description"],self["statuses_count"],self["userID"])
        return insert_sql,params

class weiboUserTagItem(scrapy.Item):
    userID = scrapy.Field()
    lables = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            UPDATE [SinaWeiboAPI].[dbo].[userFansInfoDeep] SET [lable] = %s WHERE fansID = %s
        """
        params = (self["lables"],self["userID"])
        return insert_sql,params