"""
    根据用户ID拼接URL爬取个人信息
"""
import redis

REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)


# uidFile = open('uid.txt','r')
# M_file = uidFile.readlines()
M_file = ["5355347548","3900215081","1889728690","3818859252","1616510481"]
for UID in M_file:
    user_id = UID.replace("\n","")
    print("https://m.weibo.cn/profile/info?uid=%s" % (user_id))

    REDIS_STORE.lpush("weiboUserInfoTable:start_urls","https://m.weibo.cn/profile/info?uid=%s" % (user_id))

# uidFile.close()