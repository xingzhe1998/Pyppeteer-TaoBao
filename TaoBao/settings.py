# -*- coding: utf-8 -*-

# Scrapy settings for TaoBao project
BOT_NAME = 'TaoBao'

SPIDER_MODULES = ['TaoBao.spiders']
NEWSPIDER_MODULE = 'TaoBao.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    'referer': 'https://www.taobao.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Cookies': 'thw=cn; t=9e99cdf48751aac8f39db26a957c6c18; enc=sVRv2CAh9TWhF6MUe1HpVLeuJ33nExNa7oFSziMBgLgTYang4%2F7Dys71YTFuPFkvdAScFlREKZ%2BltFTCdRZCgg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=dt88FS3j+h8CAd9oFRIPNRqF; _m_h5_tk=51b229acaadb39d794e414968fff4a44_1566491746350; _m_h5_tk_enc=4122862b2e6aac5b44ccae78deeb3658; lgc=%5Cu8BFA%5Cu79BB%5Cu7684%5Cu5C0F%5Cu4E5D%5Cu4E5D; tracknick=%5Cu8BFA%5Cu79BB%5Cu7684%5Cu5C0F%5Cu4E5D%5Cu4E5D; tg=0; v=0; cookie2=793d92f3b9c1538b0b33adb50d3689c7; _tb_token_=e0667bab3783; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; unb=2733711103; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dBy3MOS5%2BPCQ9SY24%3D&nk2=piIbCUoCYHywx5S0&id2=UU8LxdFAAmyccw%3D%3D; csg=2bfd2138; cookie17=UU8LxdFAAmyccw%3D%3D; dnk=%5Cu8BFA%5Cu79BB%5Cu7684%5Cu5C0F%5Cu4E5D%5Cu4E5D; skt=b01829699cd0430a; existShop=MTU2NjUyODkxMA%3D%3D; uc4=id4=0%40U22MwxRbdhPl0WVJFy6dGcjkDWnO&nk4=0%40pO16YVkHW9KNqXFknBZ%2BtKSlU7XpoWQ%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E4%B9%9D35; _nk_=%5Cu8BFA%5Cu79BB%5Cu7684%5Cu5C0F%5Cu4E5D%5Cu4E5D; cookie1=B0b8T6LIa0Q50Ik1kwn1uI2aR0CjQuxnajjCSU3svn0%3D; mt=ci=19_1; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=URm48syIYB3rzvI4Dim4&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTaHo52elW91w%3D%3D&tag=8&lng=zh_CN; JSESSIONID=91EA806338D5EA1BCFC9D0220A6399D3; isg=BDw8SsrgTZBHUnnNr-PE6Y34DdwuncvadjOKbRa9SCcK4dxrPkWw77JTwEk8iRi3; l=cBSxA7Huqz3ICucbBOCNZuIRXP7OSIRAiuPRwkGDi_5Cl6L1VsbOkJcZUFp62jWd9JLB4l1chow9-etXiKy06Pt-g3fP.',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}

DOWNLOADER_MIDDLEWARES = {
    'TaoBao.middlewares.PyppeteerMiddleware': 211,
#     'TaoBao.middlewares.TaobaoDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'TaoBao.pipelines.TaobaoPipeline': 211,
    'TaoBao.pipelines.MongoPipeline': 300,
}

LOG_FILE = 'TB.log'
LOG_LEVEL = 'INFO'

MONGO_URI = 'localhost'
MONGO_DB = 'TBao'