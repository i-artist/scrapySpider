# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join

class WeibobudweiserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class saveUserLookInfo(scrapy.Item):
    TweetID = scrapy.Field()
    fansID = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into [SinaWeiboAPI].[dbo].[userFansInfoDeep] ([TweetID],[fansID])
            values (%s,%s)
        """
        params = (str(self["TweetID"]),str(self["fansID"]))

class weiboUserFansInfo_Item(scrapy.Item):
    screen_name = scrapy.Field()  # 用户名
    followers_count = scrapy.Field()  # 粉丝
    follow_count = scrapy.Field()  # 关注
    verified = scrapy.Field()  # 是否认证
    verified_type = scrapy.Field()  # 认证类型
    userID = scrapy.Field()
    fansID = scrapy.Field()
    gender = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into [SinaWeiboAPI].[dbo].[userFansInfoDeep] ([userID],[fansID])
            VALUES (%s,%s)
        """

        params = (str(self["userID"]),str(self["fansID"]))
        return insert_sql,params

class weiboTWLItem(scrapy.Item):
    TweetID = scrapy.Field()
    UserID = scrapy.Field()
    UserName = scrapy.Field()
    Content = scrapy.Field()
    PostTime = scrapy.Field()
    via = scrapy.Field()
    pid = scrapy.Field()
    like = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                                INSERT INTO [SinaWeiboAPI].[dbo].[WeiBoComment_DataSource2]([TweetID],[UserID],[UserName],[mainContent],[PostTime],[pid],[via])
                                VALUES (%s, %s, %s, %s,%s,%s,%s);
                            """
        params = (
            str(self["TweetID"]), str(self["UserID"]), str(self["UserName"]), str(self["Content"]),
            str(self["PostTime"]), str(self["pid"]), str(self["via"])
        )
        return insert_sql, params

    def user_get_insert_sql(self):
        insert_sql = """
            insert into [SinaWeiboAPI].[dbo].[userFansInfoDeep] ([TweetID],[fansID])
            values (%s,%s)
        """
        params = (str(self["TweetID"]),str(self["UserID"]))

        return insert_sql,params

class weiboUserInfoDeepItem(scrapy.Item):
    screen_name = scrapy.Field()#用户名
    followers_count = scrapy.Field()#粉丝
    follow_count = scrapy.Field()#关注
    verified = scrapy.Field()#是否认证
    verified_type = scrapy.Field()#认证类型
    userID = scrapy.Field()
    fansID = scrapy.Field()
    gender = scrapy.Field()
    location = scrapy.Field()
    birthday = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            UPDATE [SinaWeiboAPI].[dbo].[userFansInfoDeep] SET [fansName] = %s,[fans_gender] = %s ,[fansBirthday] = %s,
             [fansVerified] = %s , [fansVerified_type] = %s, [fansLocation] = %s,[fans_followers_count] = %s ,
             [fans_follow_count] = %s WHERE fansID = %s
        """

        params = (str(self["screen_name"]),str(self["gender"]),str(self["birthday"]),
                  str(self["verified"]),str(self["verified_type"]),str(self["location"]),str(self["followers_count"]),
                  str(self["follow_count"]),str(self["fansID"]))

        return insert_sql,params
class weiboUserInfoItem(scrapy.Item):
    screen_name = scrapy.Field()#用户名
    followers_count = scrapy.Field()#粉丝
    follow_count = scrapy.Field()#关注
    verified = scrapy.Field()#是否认证
    verified_type = scrapy.Field()#认证类型
    verified_reason = scrapy.Field()
    uid = scrapy.Field()
    gender = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO [SinaWeiboAPI].[dbo].[WeiboUserInfo1]([screen_name],[followers_count],[follow_count],[verified],[verified_type],[uid],[gender])
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        params = (str(self["screen_name"]),str(self["followers_count"]),str(self["follow_count"]),str(self["verified"]),str(self["verified_type"]),str(self["uid"]),str(self["gender"]))

        return insert_sql,params

class weiboLocationInfoItem(scrapy.Item):
    location = scrapy.Field()
    uid = scrapy.Field()
    birthday = scrapy.Field()
    gender = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            UPDATE [SinaWeiboAPI].[dbo].[userFansInfoDeep] SET [fansLocation] = %s,[fansBirthday] = %s ,[fansGender] = %s WHERE fansID = %s
        """
        params  = (str(self['location']),str(self["birthday"]),str(self["gender"]),str(self["uid"]))
        return insert_sql,params

class weiboArticleDetailItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class weiboArticleDetailItem(scrapy.Item):
    userName = scrapy.Field()
    userIcon = scrapy.Field()
    tweetId = scrapy.Field()
    userId = scrapy.Field()
    userUrl = scrapy.Field()
    commentContent = scrapy.Field()
    orignalUser = scrapy.Field()
    orignalUserUrl = scrapy.Field()
    orignalTweetContent = scrapy.Field()
    orignalRetweet = scrapy.Field()
    orignalComment = scrapy.Field()
    orignalLike = scrapy.Field()
    orignalDevice = scrapy.Field()
    orignalTweetTime = scrapy.Field()
    commentTime = scrapy.Field()
    commentDevice = scrapy.Field()
    retweet = scrapy.Field()
    comment = scrapy.Field()
    likeCount = scrapy.Field()
    tweetUrl = scrapy.Field()
    tweetPicture = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO [SinaWeiboAPI].[dbo].[weibo_tweetDetail2] ([userName],[userIcon],[tweetId],[userId],[userUrl],
            [commentContent],[orignalUser],[orignalUserUrl],[orignalTweetContent],[orignalRetweet],[orignalComment],
            [orignalLike],[orignalDevice],[orignalTweetTime],[commentTime],[commentDevice],[retweet],[comment],
            [likeCount],[tweetUrl],[tweetPicture],[ClientID])
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            str(self["userName"]),str(self["userIcon"]),str(self["tweetId"]),str(self["userId"]),str(self["userUrl"]),
            str(self["commentContent"]),str(self["orignalUser"]),str(self["orignalUserUrl"]),
            str(self["orignalTweetContent"]),str(self["orignalRetweet"]),str(self["orignalComment"]),
            str(self["orignalLike"]),str(self["orignalDevice"]),str(self["orignalTweetTime"]),str(self["commentTime"]),
            str(self["commentDevice"]),str(self["retweet"]),str(self["comment"]),str(self["likeCount"]),
            str(self["tweetUrl"]),str(self["tweetPicture"]),'C101323'
        )

        return insert_sql,params
