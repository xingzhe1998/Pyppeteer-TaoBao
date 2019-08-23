# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CLTBSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['taobao.com']
    start_urls = ['https://s.taobao.com/search?q=华为手机']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="item next"]'),process_links='process_book_links', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pic-box-inner"]/div[@class="pic"]'), callback='parse_item', follow=True),
    )

    # 利用start_requests实现目标网站登录
    def start_requests(self):
        url = 'https://login.taobao.com/'
        yield scrapy.Request(url, callback=self.after_login, dont_filter=True)

    # 完成登录后，使用make_requests_from_url跳转到crawlspider的rule规则进行衔接
    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    @staticmethod
    def process_book_links(links):
        for link in links:
            link_url = link.url
            li  = re.findall(r'.*?ppushleft=.*?&s=(\d+)', link_url)
            if li:
                numb = int(li[0])
                if numb < 44:
                    yield link
            else:
                yield link


    def parse_item(self, response):
        print(response.url)
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
