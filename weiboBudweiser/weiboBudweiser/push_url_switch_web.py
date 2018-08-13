import redis
import re
REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)


uidFile = open('url_mid.txt','r')
M_file = uidFile.readlines()
# M_file = ["https://weibo.com/3229125510/Gs27xcGqi\n"]
for UID in M_file:
    # user_id = UID.replace("\n","")
    # print(user_id)
    # key = user_id.split("/")[-1]
    key = UID.split("?")[0].split("/")[-1]
    print("https://m.weibo.cn/status/%s" % (key))

    REDIS_STORE.lpush("weiboUrlSwitchSpiderZhong:start_urls","https://m.weibo.cn/status/%s" % (key))

# uidFile.close()