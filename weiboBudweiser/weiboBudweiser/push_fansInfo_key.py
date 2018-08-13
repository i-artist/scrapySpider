import redis
import pymssql
import hashlib
from urllib.parse import quote
REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)
# conn = pymssql.connect('123.56.196.177','shengen.zhong','zhong0000@','SinaWeiboAPI')
# cursor = conn.cursor()
# cursor.execute("SELECT fansID FROM [SinaWeiboAPI].[dbo].[userFansInfoDeep]")
# cursor.execute("SELECT fansID FROM [SinaWeiboAPI].[dbo].[userFansInfoDeep] where fansName is NULL")
# keys = [row[0] for row in cursor.fetchall()]
# uidFile = open('uid.txt','r')
# M_file = uidFile.readlines()
M_file = ["1265989743","1715991522"]
print(M_file)
for key in M_file:
    # key = key.replace("\n","")
    print(key)
    a="https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}".format(key)
    print(a)
    startUrl = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}".format(key)
    hashMD5 = hashlib.md5()
    hashMD5.update(startUrl.encode(encoding='utf-8'))
    R_status = REDIS_STORE.sadd("weibofansabcHashA:dupefilter", hashMD5.hexdigest())
    if 1 == 1:
        REDIS_STORE.lpush("userFansInfoSpiderZhongAB:start_urls",a)


# https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_2740556842

