# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymongo
from rednet.items import RednetPostItem

class RednetPipeline:

    def __init__(self, mongourl, mongoport, mongodb):
        self.mongourl = mongourl
        self.mongoport = mongoport
        self.mongodb = mongodb

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongourl=crawler.settings.get("MONGO_URL"),
            mongoport=crawler.settings.get("MONGO_PORT"),
            mongodb=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongourl, self.mongoport)
        self.db = self.client[self.mongodb]


    def process_item(self, item, spider):

        if isinstance(item, RednetPostItem):
            if self.db['rednet_post'].find({'post_id' : item['post_id']}).count() == 0:
                #record_id = self.db['rednet_post'].insert_one(item).inserted_id
                #print("Post %d has been inserted %s!" % (item['post_id'], record_id))

            else:
                #pass
                print("Post %d exist!" % item['post_id'])

        #if isinstance(item, )

        return item

    def close_spider(self, spider):
        #关闭数据库
        self.client.close()
