# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RednetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RednetPostItem(scrapy.Item):
    #mongo id
    _id = scrapy.Field()
    # 帖子名称
    name = scrapy.Field()
    # 帖子地址
    url = scrapy.Field()
    # 帖子 发帖人
    poster = scrapy.Field()
    # 帖子 发帖时间
    post_time = scrapy.Field()
    # 帖子 查看回复数量
    post_view = scrapy.Field()

    # 帖子 最新回复时间
    last_comment_time = scrapy.Field()

    # 帖子标签 可以为空
    tag = scrapy.Field()
