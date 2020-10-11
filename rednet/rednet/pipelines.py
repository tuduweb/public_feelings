# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymongo

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

        if isinstance(item, DoubanItem):
            if self.db['db_movie'].find({'movie_id' : item['movie_id']}).count() == 0:
                post_id = self.db['db_movie'].insert_one(item).inserted_id
                print("Movie %d inserted %s!" % (item['movie_id'], post_id))

            else:
                print("Movie %d exist!" % item['movie_id'])

        return item

    def close_spider(self, spider):
        #关闭数据库
        self.client.close()
