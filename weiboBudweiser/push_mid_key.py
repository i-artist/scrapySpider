import redis

REDIS_STORE = redis.Redis(host='123.56.196.177', port=6379)
keys = ["4256265766957090","4264523881773397","4268847185973417","4240431321328794","4259835052790412","4267056151386886",
        "4252276581651743","4259429157267796","4257411440730885","4247119067871662","4265729924611579","4265791589316137",
        "4265729924611579"]
for key in keys:


    if 1 == 1:

        REDIS_STORE.lpush("weiboArticleDetailSpiderZhong:start_urls", "https://m.weibo.cn/status/{}".format(key))
        # push到评论信息

        REDIS_STORE.lpush("weiboCommentSpiderZhong:start_urls",
                                   "https://m.weibo.cn/api/comments/show?id={}&page=1".format(key))
        # push到点赞信息

        REDIS_STORE.lpush("weiboLikeSpiderZhong:start_urls",
                                   "https://m.weibo.cn/api/attitudes/show?id={}&page=1".format(key))
        # push到转发信息

        REDIS_STORE.lpush("weiboRetweetSpiderZhong:start_urls",
                                   "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(key))
