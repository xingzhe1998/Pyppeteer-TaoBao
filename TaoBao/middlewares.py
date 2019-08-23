# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random
import asyncio
import pyppeteer
import logging
from logging import getLogger
import json
from scrapy import signals
from pyppeteer import launch
from scrapy.http import HtmlResponse
from concurrent.futures._base import TimeoutError

pyppeteer_level = logging.WARNING
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)


class PyppeteerMiddleware(object):

    js1 = '''() =>{Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});}'''
    js2 = '''() =>{Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5,6],});}'''
    js3 = 'window.scrollTo(0,document.body.scrollHeight)'

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.getbrowser())
        self.loop.run_until_complete(task)

    async def getbrowser(self):
        self.browser = await launch(
            headless=False,
            # userDataDir='uData',
            args=[
                '--disable-infobars',
                '--window-size=1366,850',
            ],
        )
        self.page = await self.browser.newPage()
        await self.page.emulate(
            viewport={'width': 1366, 'height': 768},
            userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        )
        self.page.setDefaultNavigationTimeout = 0

    async def intercept_request(self, req):
        """
        请求过滤
        有一个小问题需要注意，在登录时，可能会出现验证码
        用这个方法拦截的时候，会把验证码给拦截
        从而程序无法定位验证码元素会报错
        """
        if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
            await req.abort()
        else:
            await req.continue_()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        try:
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.login(request))
            loop.run_until_complete(task)
            return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8", request=request, status=200)
        except TimeoutError as ex:
            print('download page fail...', request.url)
            return HtmlResponse(url=request.url, request=request, status=404)

    async def login(self, request):
        if request.url != 'https://login.taobao.com/':
            await self.page.setRequestInterception(True)
            self.page.on('request', self.intercept_request)    # 拦截图片视频等加载
            navigationPro = asyncio.ensure_future(self.page.waitForNavigation(timeout=0))
            await self.page.goto(request.url)
            await navigationPro
            await self.page.evaluate(PyppeteerMiddleware.js3)  # 下滑
            await self.page.reload()
            items = await self.page.waitForXPath('//div[contains(@class,"item J_MouserOnverReq")]')
            await self.page.waitFor(2000+random.random()*2000)
            content = await self.page.content()
            return content
        else:
            # await self.page.setRequestInterception(False)      # 避免拦截验证码出错，关闭拦截
            await self.page.goto(request.url)
            await self.page.evaluate(PyppeteerMiddleware.js1)  # 修改识别参数
            await self.page.evaluate(PyppeteerMiddleware.js2)  # 修改识别餐素
            buttom = await self.page.querySelector('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
            if buttom:
                await self.page.waitForSelector('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
                await self.page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
            await self.page.waitForSelector('#TPL_username_1')
            await self.page.hover('#TPL_username_1')
            await self.page.click('#TPL_username_1')
            await self.page.keyboard.type('诺离的小九九', delay=random.random() * 600)  # 控制输入速度
            await self.page.waitFor(random.random() * 400)  # milliseconds
            await self.page.hover('#TPL_password_1')
            await self.page.click('#TPL_password_1')
            await self.page.keyboard.type('xyz998123.', delay=random.random() * 600)  # 控制输入速度
            await self.page.waitFor(random.random() * 800)
            navigationPromise = asyncio.ensure_future(self.page.waitForNavigation(timeout=0))
            await self.page.click('#J_SubmitStatic')                                  # 点击鼠标可能会出现验证码/我的淘宝
            await navigationPromise                                                   # login登录时输入过快，会出现验证码
            slider_pd = await self.page.querySelector('#nc_1__scale_text > span')
            if slider_pd:
                print('捕获验证码')
                slider_width = await self.page.querySelectorEval('#nc_1__scale_text > span', 'node => node.offsetWidth')  # {}
                s_width = await self.page.querySelectorEval('#nc_1_n1z', 'node => node.offsetWidth')
                await self.page.waitFor(random.random() * 500)  # milliseconds
                await self.page.click('#nc_1_n1z')
                await self.page.hover('#nc_1_n1z')
                # print(s_width)  # 42
                await self.page.mouse.down()
                # print(slider_width)  # 298
                # x = slider_width-s_width
                await self.page.mouse.move(x=(slider_width - s_width) * 10, y=0, step=10)  # 真实长度为298 - 42
                await self.page.waitFor(random.random() * 500)  # milliseconds
                await self.page.mouse.up()  # 释放鼠标会需要重新输入密码
                await self.page.hover('#TPL_password_1')
                await self.page.click('#TPL_password_1')
                await self.page.keyboard.type('xyz998123.', delay=random.random() * 400)  # 控制输入速度
                await self.page.waitFor(random.random() * 600)
                navigationPromise = asyncio.ensure_future(self.page.waitForNavigation(timeout=0))
                await self.page.click('#J_SubmitStatic')  # 点击鼠标可能会出现验证码/我的淘宝
                await navigationPromise
                print('验证码破解成功')
            else:
                print('未出现验证码')
            content = await self.page.content()
            cookies_list = await self.page.cookies()
            with open('cookies.txt', 'w+', encoding='utf-8') as fp:
                fp.write(json.dumps(cookies_list))
            return content

    def __del__(self):
        print('正在关闭loop...')
        self.loop.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class TaobaoSpiderMiddleware(object):
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


class TaobaoDownloaderMiddleware(object):
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
