# -*- coding: utf-8 -*-
import re
import random
import scrapy
import time
import json
from TaoBao.items import TaobaoItem
from scrapy.spiders import Spider
import urllib.parse

class TbSpider(Spider):
    name = 'tb'
    allowed_domains = ['taobao.com']
    start_urls = ['https://www.taobao.com/']
    keywords = ['华为手机', '小米手机']

    def start_requests(self):
        url = 'https://login.taobao.com/'
        yield scrapy.Request(url, callback=self.get_page_url)

    def get_page_url(self, response):
        cookies = {}
        with open('cookies.txt', 'r', encoding='utf-8') as fp:
            j_cookies = fp.read()
            cookies_list = json.loads(j_cookies)
            for cookie in cookies_list:
                cookies[cookie['name']] = cookie['value']
        # print(cookies)
        for keyword in TbSpider.keywords:
            for i in range(0, 100):
                base_url = 'https://s.taobao.com/search?q={0}&bcoffset=1&ntoffset=1&p4ppushleft=1%2C48&s={1}'.format(keyword, i*44)
                time.sleep(3+random.random())
                yield scrapy.Request(url=base_url, cookies=cookies, callback=self.parse_page_info, dont_filter=True)

    def parse_page_info(self, response):
        print('response.status-> ', response.status)
        print('response.url-> ', response.url)
        # print('response.body-> ', response.body)
        values_item = response.xpath('//div[contains(@class,"item J_MouserOnverReq")]')
        for value in values_item:
            item = TaobaoItem()
            li = re.findall('.*?q=(.*?)&.*', response.url)
            if urllib.parse.unquote(li[0]) == '华为手机':    # url中文解码
                item['commodity_type'] = '华为手机'
            elif urllib.parse.unquote(li[0]) == '小米手机':
                item['commodity_type'] = '小米手机'
            item['commodity_shop'] = value.xpath('.//div[@class="shop"]/a/span[not(@class)]/text()').get()
            item['commodity_price'] = '¥' + value.xpath('.//div[@class="price g_price g_price-highlight"]/strong/text()').get()
            commodity_title_lis = value.xpath('.//div[@class="row row-2 title"]/a//text()').getall()
            cc_lis = list(map(lambda x:re.sub('[\n\s]', '', x), commodity_title_lis))
            vc_lis = [val for val in cc_lis if val!='']
            item['commodity_title'] = ''.join(vc_lis)
            item['commodity_img_url'] = 'https:' + value.xpath('.//div[@class="pic"]/a/img/@data-src').get()
            item['commodity_shop_url'] = value.xpath('.//div[@class="shop"]/a/@href').get()                  # 添加https: 并且添加判断
            item['commodity_detail_url'] = value.xpath('.//div[@class="pic"]/a/@href').get()                 # 添加https: 并且添加判断
            item['commodity_shop_place'] = value.xpath('.//div[@class="location"]/text()').get()
            item['commodity_payment_number'] = value.xpath('.//div[@class="deal-cnt"]/text()').get()
            yield item
