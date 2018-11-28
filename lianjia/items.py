# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    #序号
    serial_number = scrapy.Field()
    #名称
    house_name = scrapy.Field()
    #区域 大区
    area = scrapy.Field()
    #区域 中区
    position = scrapy.Field()
    #小区名
    region = scrapy.Field()
    # 总价
    total = scrapy.Field()
    # 单价
    unitprice = scrapy.Field()
    # 面积
    square = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 户型
    shape = scrapy.Field()
    # 关注状况
    followinfo = scrapy.Field()