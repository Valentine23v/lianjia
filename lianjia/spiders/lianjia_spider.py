# -*- coding: utf-8 -*-
import json
from lxml import etree
import scrapy
from lianjia.items import LianjiaItem
import string

class LianjiaSpiderSpider(scrapy.Spider):
    #计数页数
    def __init__(self):
        self.pagecount = 0
    #爬虫名 和项目名不重复
    name = 'lianjia_spider'
    #允许的域名
    allowed_domains = ['qd.lianjia.com']
    #入口URL，放到调度器里
    start_urls = ['https://qd.lianjia.com/ershoufang/shibei']

    def parse(self, response):
        house_list = response.xpath("//div[@class='leftContent']/ul[@class='sellListContent']/li[@class='clear LOGCLICKDATA']")
        # self.pagecountcount += 1
        #print(response.text)

        count=0
        for i_item in house_list:

            lianjia_item = LianjiaItem()
            #序号
            count = count + 1  # 从第一个开始
            lianjia_item['serial_number'] = self.pagecount * 30 + count#第几条
            #名称
            lianjia_item['house_name'] = i_item.xpath(".//div[@class='info clear']/div[@class='title']/a/text()").extract_first()#第一个title 大陆版名称
            # 默认
            # lianjia_item['area'] = "市北"
            # 区域 中区
            lianjia_item['position'] = i_item.xpath(".//div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/a/text()").extract_first()
            # 小区名
            lianjia_item['region'] = i_item.xpath(".//div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/a/text()").extract_first()
            # 总价
            lianjia_item['total'] = i_item.xpath(".//div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice']/span/text()").extract_first()
            # 单价
            lianjia_item['unitprice'] = i_item.xpath(".//div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()").extract_first()
            # 面积户型朝向装修情况电梯
            content = i_item.xpath(".//div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()").extract_first()
            content_s=content.split(" | ")
            del (content_s[0])  # 第一个是空的删掉
            # print(content_s)
            #面积
            lianjia_item['square'] = content_s[1]
            # 户型
            lianjia_item['shape'] = content_s[0]
            # 朝向装修电梯略
            # 年代
            # posinfo = i_item.xpath(".//div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/text()").extract_first()
            # if posinfo.find("建")!=-1:
            #     lianjia_item['year'] = posinfo.split("年")[0].split(")")[1]
            # else:
            #     pass
            # print("年代:"+lianjia_item['year']+"年")
            # 关注状况 关注带看发布时间/后续补充分隔开
            lianjia_item['followinfo'] = i_item.xpath(".//div[@class='info clear']/div[@class='followInfo']/text()").extract_first()

            # 输出
            # print("序号:" + str(lianjia_item['serial_number']))
            # print("简介:" + lianjia_item['house_name'])
            # print("区域:" + lianjia_item['position'])
            # print(lianjia_item['region'])
            # print("总价:" + lianjia_item['total'] + "万")
            # print(lianjia_item['unitprice'])
            # print("面积"+lianjia_item['square'])
            # print(lianjia_item['shape'])
            # print(lianjia_item['followinfo'])

             #数据要yeild放到管道里
            yield lianjia_item



        selector = etree.HTML(response.text)
        pagestr = selector.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]  # 返回的是字符串字典
        pageobj = json.loads(pagestr)  # 转化为字典
        total_pages = pageobj.get("totalPage")
        self.pagecount = pageobj.get("curPage")-1
        # print(self.pagecount,"/",total_pages)

        # 循环
        for page in range(1,int(total_pages)+1):
            url_page = "https://qd.lianjia.com/ershoufang/pg{}/".format(str(page + 1))
            # print(url_page)
            yield scrapy.Request(url=url_page, callback=self.parse)#回调parse
