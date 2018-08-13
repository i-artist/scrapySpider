"""
    根据用户ID爬取所有微博mid
"""
import redis
import pymssql
import hashlib
REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)
# conn = pymssql.connect('123.56.196.177','shengen.zhong','zhong0000@','SinaWeiboAPI')
# cursor = conn.cursor()
# cursor.execute("SELECT uid FROM [SinaWeiboAPI].[dbo].[WeiboUserInfo1] WHERE followers_count>1000 and followers_count<15000 and (verified_type='0' or verified_type='-1')")
# keys = [row[0] for row in cursor.fetchall()]


uidFile = open('uid.txt','r')
M_file = uidFile.readlines()
M_file = ["5355347548","3900215081","1889728690","3818859252","1616510481"]
print(M_file)
for key in M_file:
    # key.replace("\n","")
    print("https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(key))
    startUrl = "https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(key)
    hashMD5 = hashlib.md5()
    hashMD5.update(startUrl.encode(encoding='utf-8'))
    R_status = REDIS_STORE.sadd("weiboPersorTweetAllHashTestZZ:dupefilter", hashMD5.hexdigest())
    if 1 == 1:
        REDIS_STORE.lpush("weiboPersonTweetAllSpiderZhong:start_urls","https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(key))


# with open('uidArticle.txt','r') as M_file:
#     M_f = M_file.readlines()
#     for M_uid in M_f:
#         uid = M_uid.replace("\n","")
#         print("https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(uid))
#         startUrl = "https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(uid)
#         hashMD5 = hashlib.md5()
#         hashMD5.update(startUrl.encode(encoding='utf-8'))
#         R_status = REDIS_STORE.sadd("weiboPersorTweetAllHashTest:dupefilter", hashMD5.hexdigest())
#         if 1 == R_status:
#             REDIS_STORE.lpush("weiboPersonTweetAllTest:start_urls",
#                               "https://m.weibo.cn/api/container/getIndex?containerid=230413{}&page=1".format(uid))
#
