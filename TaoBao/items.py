# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    commodity_type = scrapy.Field()
    commodity_img_url = scrapy.Field()
    commodity_payment_number = scrapy.Field()
    commodity_price = scrapy.Field()
    commodity_title = scrapy.Field()
    commodity_shop = scrapy.Field()
    commodity_shop_url = scrapy.Field()
    commodity_shop_place = scrapy.Field()
    commodity_detail_url = scrapy.Field()
