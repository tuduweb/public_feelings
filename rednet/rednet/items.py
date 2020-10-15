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
    # 帖子ID
    post_id = scrapy.Field()
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


class RednetPostCommentItem(scrapy.Item):
    #mongo id
    _id = scrapy.Field()
    #no name
    #content

    #floor 帖子楼层
    floor = scrapy.Field()

    #comment id
    comment_id = scrapy.Field()
    #回帖人
    comment_poster = scrapy.Field()

    #content 里面的内容还可以找出回复引用的关系
    comment_content = scrapy.Field()

    '''
    <i class="pstatus"> 本帖最后由 不服投个票A 于 2017-12-14 12:18 编辑 </i>
    '''

    #支持 反对
    vote_agree = scrapy.Field()
    vote_disagree = scrapy.Field()

    #附件相关 是否有附件..
    has_attachments = scrapy.Field()

    ''' https://bbs.rednet.cn/forum.php?mod=viewthread&tid=47390167&extra=page%3D1%26filter%3Dtypeid%26typeid%3D2869%26orderby%3Ddateline
    <div class="pattl">
    <ignore_js_op>
    <dl class="tattl attm">
    <dt></dt>
    <dd>
    <p class="mbn">
    '''

    attachments_list = scrapy.Field()