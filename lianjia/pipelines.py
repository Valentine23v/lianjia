# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from lianjia.settings import mongo_host,mongo_port,mongodb_name,mongodb_collection

class LianjiaPipeline(object):


    # 连接mongodb
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongodb_name
        sheetname = mongodb_collection

        client = pymongo.MongoClient(host=host,port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item) # item 是spider 里 yeild来的
        self.post.insert(data)
        return item
