# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
import requests
from scrapy import signals
from weiboBudweiser.useragent import agents
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
class WeibobudweiserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeibobudweiserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
class UserAgentMiddleware(object):
    def __init__(self):
        # self.UA = UserAgent()
        pass
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        request.headers["Upgrade-Insecure-Requests"] = 1

        # cookieText = requests.get("http://139.196.114.157:5656/weiboPC/cookie")
        if True:
            # cookie = json.loads(BeautifulSoup(cookieText.text, "lxml").get_text())
            # a={'SINAGLOBAL':'4528592796080.031.1520908752947', 'YF-Ugrow-G0':'5b31332af1361e117ff29bb32e4d8439',
            #             #    'YF-V5-G0':'cd5d86283b86b0d506628aedd6f8896e', 'YF-Page-G0':'ed0857c4c190a2e149fc966e43aaf725',
            #             #    '_s_tentry':'login.sina.com.cn', 'Apache':'9082888879053.594.1532927175550', 'ULV':'1532927175591:14:3:1:9082888879053.594.1532927175550:1532312820190',
            #             #    'login_sid_t':'62a12e38644c7b0e0fdff0a6d395ea35', 'cross_origin_proto':'SSL', 'un':'953665604@qq.com', 'UOR':',,login.sina.com.cn; wb_view_log=1920*10801',
            #             #    'ALF':'1565319010', 'SSOLoginState':'1533783011', 'SCF':'AjPSbBYuB7v4M5AKuvUhjcdwF4MsHLWg277o23JJi4hJY3OYLQGAk3EB7VDVf3PYHEI8ugE-DJpIDWz_uE4_QQ4.',
            #             #    'SUB':'_2A252b9u0DeRhGedJ71YW9ibKwzuIHXVVHUp8rDV8PUNbmtBeLXL_kW9NVh1CXR8gNzoqA8v_rn27qUC6NThs1cNc',
            #             #    'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFiTcJJ0iupzPRKIWU6nz5L5JpX5KzhUgL.Fo2NShBNSonc1hM2dJLoIEBLxKML1K.LB.-LxK-LBKnL1h2LxK-L1K-LBKBLxK.L1h-L1Kzt',
            #             #    'SUHB':'0JvxFLZIoc6tyf', 'wb_view_log_1744768687':'1920*10801'}
            a = {
                'SINAGLOBAL':'4528592796080.031.1520908752947', 'YF-Ugrow-G0':'5b31332af1361e117ff29bb32e4d8439',
                'YF-V5-G0':'cd5d86283b86b0d506628aedd6f8896e', 'YF-Page-G0':'ed0857c4c190a2e149fc966e43aaf725',
                '_s_tentry':'login.sina.com.cn', 'Apache':'9082888879053.594.1532927175550',
                'ULV':'1532927175591:14:3:1:9082888879053.594.1532927175550:1532312820190',
                'login_sid_t':'62a12e38644c7b0e0fdff0a6d395ea35', 'cross_origin_proto':'SSL', 'un':'953665604@qq.com',
                'SSOLoginState':'1533783011', 'UOR':',,www.baidu.com', 'wb_view_log_1744768687':'1920*10801%261366*7681',
                'SCF':'AjPSbBYuB7v4M5AKuvUhjcdwF4MsHLWg277o23JJi4hJZZq45c870AXUTQfC3_a06lx5iWMiwk3IcnfwJ4fUXOw.',
                'SUB':'_2A252aXMqDeRhGedJ71YW9ibKwzuIHXVVH-PirDV8PUNbmtBeLUbfkW9NVh1CXYbEYBKyfmzex7gMEdNe59UaA17d',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFiTcJJ0iupzPRKIWU6nz5L5JpX5KMhUgL.Fo2NShBNSonc1hM2dJLoIEBLxKML1K.LB.-LxK-LBKnL1h2LxK-L1K-LBKBLxK.L1h-L1Kzt',
                'SUHB':'0u5A0TbIDfx-g9', 'ALF':'1565406967', 'wvr':'6'
            }
            request.cookies = a
            request.headers['Cookie'] = a

        # request.meta["proxy"] = "https://110.72.150.245:8123"
