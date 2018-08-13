import redis
import pymssql
import hashlib
REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)
conn = pymssql.connect('123.56.196.177','shengen.zhong','zhong0000@','SinaWeiboAPI')
cursor = conn.cursor()
cursor.execute("SELECT fansID FROM [SinaWeiboAPI].[dbo].[userFansInfoDeep] where createtime>'2018-08-08 00:00:00' and fansName is NULL")
keys = [row[0] for row in cursor.fetchall()]
print(keys)
for key in keys:
    print("https://m.weibo.cn/profile/info?uid={}".format(key))
    startUrl = "https://m.weibo.cn/profile/info?uid={}".format(key)
    hashMD5 = hashlib.md5()
    hashMD5.update(startUrl.encode(encoding='utf-8'))
    R_status = REDIS_STORE.sadd("weibofansabcHashzzhh:dupefilter", hashMD5.hexdigest())
    if 1 == 1:
        REDIS_STORE.lpush("weiboPersonInfoSpiderZhong:start_urls","https://m.weibo.cn/profile/info?uid={}".format(key))

