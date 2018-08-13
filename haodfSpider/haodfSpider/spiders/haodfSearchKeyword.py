# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy
import json
import redis
from haodfSpider.settings import REDIS_HOST,REDIS_PORT
from haodfSpider.items import HaodfKeywordDetailItem
class HaodfsearchkeywordSpider(scrapy.Spider):
    name = 'haodfSearchKeyword'
    allowed_domains = ['mobile-api.haodf.com']
    start_urls = ['http://mobile-api.haodf.com/11','http://mobile-api.haodf.com/22','http://mobile-api.haodf.com/33']
    REDIS_STORE = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def start_requests(self):
        url = 'http://mobile-api.haodf.com/patientapi/user_search4new'
        keys = ["","","大便难","linzess","linaclotide","","","","",
                "","","","","","",""
        ]
        #     IBS-C 开塞露 Prucalopride 麻仁丸 比沙可啶 乳果糖 普卡比利 鲁比前列酮 便秘型肠易激综合征 lubiprostone 利那洛肽 便秘 大便干
        yield scrapy.FormRequest(
            url = url,
            formdata = {"app":"p","sv":"8.1.0","os":"android","di":"867130038434664","pageSize":"10","targetType":"article",
                        "pageId":"30","userId":"0","m":"EML-AL00","n":"2","deviceToken":"867130038434664","p":"2","currentUserId":"0",
                        "s":"hw","v":"5.8.6","api":"1.2","key": "大便干"},
            callback = self.parse,
            meta = {"currentPage" : 30,"keyWord":"大便干"}
        )

    def parse(self, response):
        haodfData = json.loads(response.text)
        ArticleList = haodfData["content"]["items"]
        currentPage = response.meta["currentPage"]
        keyWord = response.meta["keyWord"]
        if len(ArticleList) == 0:
            pass
        else:
            for item_D in ArticleList:
                try:
                    id = item_D["data"]["id"]
                    print(id)
                    yield scrapy.FormRequest(
                        url = 'http://mobile-api.haodf.com/patientapi/article_getArticleIntroByArticleId',
                        formdata = {
                            "app":"p","sv":"8.1.0","os":"android","di":"867130038434665","articleId":id,"m":"EML-AL00",
                            "userId":"","n":"2","deviceToken":"867130038434665","p":"2","s":"hw","currentUserId":"0",
                            "_t":"","v":"5.8.6","api":"1.2"
                        },
                        callback = self.parse_detail,
                        meta = {"articleId":id,"grade":item_D["data"]["grade"],"hospitalForArticle":item_D["data"]["hospitalForArticle"],"keyword":keyWord}
                    )
                except:
                    pass
            currentPage = currentPage + 1
            yield scrapy.FormRequest(
                url=response.url,
                formdata={"app": "p", "sv": "8.1.0", "os": "android", "di": "867130038434665", "pageSize": "30",
                          "targetType": "article",
                          "pageId": str(currentPage), "userId": "0", "m": "EML-AL00", "n": "2", "deviceToken": "867130038434665",
                          "p": "2", "currentUserId": "0",
                          "s": "hw", "v": "5.8.6", "api": "1.2", "key": keyWord},
                callback=self.parse,
                meta={"currentPage": currentPage,"keyWord":keyWord}
            )

        pass

    def parse_detail(self,response):
        keyword = response.meta["keyword"]
        haodf_item = HaodfKeywordDetailItem()
        haodf_item["keyword"] = keyword
        haodf_item["grade"] = response.meta["grade"]
        haodf_item["hospitalForArticle"] = response.meta["hospitalForArticle"]
        haodfDetail = json.loads(response.text)
        htmlData = haodfDetail["content"]["content"]
        soup = BeautifulSoup(htmlData,'lxml')
        try:
            haodf_item["comment"] = soup.select("div[class=\"d-c-content\"]")[0].text
        except:
            haodf_item["comment"] = " "
        haodf_item["doctorId"] = haodfDetail["content"]["doctorId"]
        haodf_item["doctorName"] = haodfDetail["content"]["doctorName"]
        haodf_item["articleId"] = response.meta["articleId"]
        haodf_item["postTime"] = soup.select("span[class=\"d-i-d-label\"]")[0].text
        haodf_item["pageView"] = soup.select("span[class=\"d-i-d-label\"]")[-1].text.strip()[0:-3]
        haodf_item["articleContent"] = soup.select("div[class=\"webtxt\"]")[0].text.split("})")[-1]
        yield haodf_item
