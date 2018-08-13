import scrapy
from YiYaoWang.items import YiYaoWangCommentItem

class YiYaoWangSpider(scrapy.Spider):
    name = "YiYaoWangSpider"
    allowed_domain = "www.111.com.cn"
    start_urls = [
        "http://www.111.com.cn/product/971660.html",
        "http://www.111.com.cn/product/50088521.html",
        "http://www.111.com.cn/product/5423544.html",
        "http://www.111.com.cn/product/50716522.html",
        "http://www.111.com.cn/product/50090912.html",
        "http://www.111.com.cn/product/50096856.html"
    ]

    def parse(self,response):
        goodID = response.url.split("/")[-1][:-5]
        yield scrapy.Request(
            url = "http://www.111.com.cn/interfaces/review/list/html.action?goodsId={}&pageIndex=1&score=&_18081311".format(goodID),
            callback = self.commentParse,
            meta = {"url":response.url}
        )
    def commentParse(self,response):
        if response.text == '110.error':
            pass
        else:
            Url = response.meta["url"]
            comment_C = response.css("td p:nth-of-type(1)::text").extract()
            comment_D = response.css("td p:nth-of-type(2)::text").extract()
            for index in range(len(comment_C)):
                YiYao_item = YiYaoWangCommentItem()
                try:
                    YiYao_item["commentContent"] = comment_C[index]
                except:
                    YiYao_item["commentContent"] = ""
                try:
                    YiYao_item["commentDate"] = comment_D[index]
                except:
                    YiYao_item["commentDate"] = ""
                YiYao_item["url"] = Url

                yield YiYao_item

            currentPage = response.url.split("&pageIndex=")[-1].split("&")[0]
            currentUrl = response.url.split("&pageIndex=")[0]
            currentPage = int(currentPage) + 1
            yield scrapy.Request(
                url = "{}&pageIndex={}&score=&_18081311".format(currentUrl,currentPage),
                callback = self.commentParse,
                meta = {"url":Url}
            )