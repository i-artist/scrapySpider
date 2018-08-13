# -*- coding: utf-8 -*-
__author__ = 'zhong'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "weiboInfoDeepSpider"])
# execute(["scrapy", "crawl", "weiboTweetComment"])
# execute(["scrapy", "crawl", "weiboInfoSpider"])
# execute(["scrapy", "crawl", "weiboArticleListSpider"])
# execute(["scrapy", "crawl", "weiboArticleDetailSpiderZZ"])
# execute(["scrapy", "crawl", "weiboPCSearchURL"])
# execute(["scrapy", "crawl", "weiboLocationInfo"])
execute(["scrapy", "crawl", "weiboUserFansPC"])
# execute(["scrapy", "crawl", "weiboUrlSwitchZhong"])




