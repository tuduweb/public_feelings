# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanPipeline:
#    def __init__(self, mongo_uri, mongo_db)
#        self.mongo_uri = mongo_uri
#        self.mongo_db = mongo_db
#        self.col = 'some'
    def process_item(self, item, spider):
        return item
