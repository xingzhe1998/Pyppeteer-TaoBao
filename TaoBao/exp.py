# # -*- coding: utf-8 -*-
# #crawspider登陆豆瓣，爬取豆瓣电影top250
#
# import scrapy
# import urllib
# from PIL import Image
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.loader import ItemLoader
# from douban.items import Movietop250
#
#
# class Movietop250LoginCrawlspiderSpider(CrawlSpider):
#     name = 'movieTop250_login_crawlspider'
#     allowed_domains = ['douban.com']
#     start_urls = ['https://movie.douban.com/top250']
#
#     headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
#
#     rules = (
#         Rule(LinkExtractor(allow='start=[0-5][0-5]&filter=')),
#         Rule(LinkExtractor(allow='/subject/\d+/'), callback='parse_item'),
#     )
#
#     def start_requests(self):
#     '''
#     重写start_requests，请求登录页面
#     '''
#     return [scrapy.FormRequest("https://accounts.douban.com/login", headers=self.headers, meta={"cookiejar":1}, callback=self.parse_before_login)]
#
#     def parse_before_login(self, response):
#     '''
#     登录表单填充，查看验证码
#     '''
#     print("登录前表单填充")
#     captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
#     captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
#     if captcha_image_url is None:
#         print("登录时无验证码")
#         formdata = {
#                 "source": "index_nav",
#                 "form_email": "yanggd1987@163.com",
#                 "form_password": "******",
#             }
#     else:
#         print("登录时有验证码")
#         save_image_path = "/home/yanggd/python/scrapy/douban/douban/spiders/captcha.jpeg"
#         #将图片验证码下载到本地
#         urllib.urlretrieve(captcha_image_url, save_image_path)
#         #打开图片，以便我们识别图中验证码
#         try:
#             im = Image.open('captcha.jpeg')
#             im.show()
#         except:
#             pass
#
#         #手动输入验证码
#         captcha_solution = raw_input('根据打开的图片输入验证码:')
#         formdata = {
#                 "source": "None",
#                 "redir": "https://www.douban.com",
#                 "form_email": "yanggd1987@163.com",
#                                 "form_password": "******",
#                 "captcha-solution": captcha_solution,
#                 "captcha-id": captcha_id,
#                 "login": "登录",
#             }
#
#
#     print("登录中")
#     #提交表单
#     return scrapy.FormRequest.from_response(response, meta={"cookiejar":response.meta["cookiejar"]}, headers=self.headers, formdata=formdata, callback=self.parse_after_login)
#
#     def parse_after_login(self, response):
#     '''
#     验证登录是否成功,通过make_requests_from_url对接crawlspider
#     '''
#     account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
#     if account is None:
#         print("登录失败")
#     else:
#         print(u"登录成功,当前账户为 %s" %account)
#         #在此通过make_requests_from_url进入rules
#         for url in self.start_urls :
#             yield self.make_requests_from_url(url)
#
#     def parse_item(self, response):
#     loader = ItemLoader(item=Movietop250(), selector=response.xpath('//div[@id="content"]'))
#     #loader.add_xpath('rank', 'h1/span[@property="v:itemreviewed"]/text()')
#     #yield loader.load_item()
#     loader = ItemLoader(item=Movietop250(), selector=response)
#     movie = loader.nested_xpath('//div[@id="content"]')
#     movie.add_xpath('rank', 'div[@class="top250"]/span[@class="top250-no"]/text()')
#     movie.add_xpath('title', 'h1/span[@property="v:itemreviewed"]/text()')
#     yield loader.load_item()



# <----------------------------------------////----------------------------------------->
# 重载start_requests方法
# def start_requests(self):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}
#     # 指定cookies
#     cookies = {
#         'uuid': '66a0f5e7546b4e068497.1542881406.1.0.0',
#         '_lxsdk_cuid': '1673ae5bfd3c8-0ab24c91d32ccc8-143d7240-144000-1673ae5bfd4c8',
#         '__mta': '222746148.1542881402495.1542881402495.1542881402495.1',
#         'ci': '20',
#         'rvct': '20%2C92%2C282%2C281%2C1',
#         '_lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorganic',
#         '_lxsdk_s': '1674f401e2a-d02-c7d-438%7C%7C35'}
#
#     # 再次请求到详情页，并且声明回调函数callback，dont_filter=True 不进行域名过滤，meta给回调函数传递数据
#     yield Request(detailUrl, headers=headers, cookies=cookies, callback=self.detail_parse, meta={'myItem': item},
#                   dont_filter=True)




# elif request.url != 'https://login.taobao.com/' and 'detail' in request.url:
#     await self.page.setRequestInterception(True)
#     self.page.on('request', self.intercept_request)
#     await self.page.goto(request.url)
#     content = await self.page.content()
#     return content