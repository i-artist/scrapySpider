## MobileNew 
爬取的网址为http://shouji.tenaa.com.cn/Mobile/MobileNew.aspx <br>
把手机的详情爬取下来，并把手机图片保存到对应的文件夹内。
## haodfSpider
爬取的APP 好大夫在线<br>
通过fiddle进行手机的抓包，拿到参数然后拼接请求，处理返回的json数据。APP升级代码可能会失效，但整体逻辑还是一样的。
## YiYaoWang
爬取的网站为一药网，爬取的内容是商品的评价内容

## weiboBudweiser
爬取的网站是新浪微博 （移动端接口）。<br>
因为微博数据量的庞大，所以采取了使用redis进行分布式的爬取，对爬取的url进行hashlib的去重，请求携带的cookie池是使用python的Flask搭建的（其实不携带cookie也可以，设置下载延迟，部署到不同的服务器），在数据的存储的pipelines使用了异步存储，提高了存储的效率。<br>
#需要微博自动发私信（商业邀请），自动评论，微博账号自动识别验证码登录等一些自动化脚本可以加 WX zhong_888520详谈

