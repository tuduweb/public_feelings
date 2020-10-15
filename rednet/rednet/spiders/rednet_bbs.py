import scrapy


from urllib import parse
from rednet.items import RednetPostItem, RednetPostCommentItem


class RednetBbsSpider(scrapy.Spider):
    name = 'rednet_bbs'
    allowed_domains = ['rednet.cn']
    start_urls = ['https://bbs.rednet.cn/forum.php?mod=forumdisplay&fid=81&filter=author&orderby=dateline']

    def parse(self, response):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_list)

    def parse_list(self, response):
        post_list = response.xpath("//tbody[contains(@id, 'normalthread_')]")


        for i_item in post_list:

            post_item = RednetPostItem()

            post_item['name'] = i_item.xpath(".//tr/th/a/text()").extract_first()
            print(post_item['name'])

            post_item['url'] = i_item.xpath(".//tr/th/a/@href").extract_first()
            print(post_item['url'])

            result = parse.urlparse(post_item['url'])
            post_id = parse.parse_qs(result.query).get("tid", [])[0]
            post_item['post_id'] = post_id

            post_item['tag'] = i_item.xpath(".//tr/th/em/a/text()").extract_first()
            print(post_item['tag'])

            post_item['poster'] = i_item.xpath(".//tr/td[@class='by']/cite/a/@href").extract_first()
            print(post_item['poster'])

            # TODO:采集的时间有问题,待修改
            # 帖子 发帖时间（可能进入页面后还会有更新的回复）
            post_item['post_time'] = i_item.xpath(".//tr/td[@class='by']/em/a/text()").extract_first()
            print(post_item['post_time'])

            # 帖子 本次采集的最新回复时间（可能进入页面后还会有更新的回复）
            post_item['last_comment_time'] = i_item.xpath(".//tr/td[@class='by'][last()]/em/a/text()").extract_first()
            print(post_item['last_comment_time'])

            post_view_item = i_item.xpath(".//tr/td[@class='num']")
            post_item['post_view'] = { post_view_item.xpath(".//a/text()").extract_first(),
                          post_view_item.xpath(".//em/text()").extract_first()}

            print(post_item['post_view'])

            if post_item['url'] is not None:
                yield response.follow(post_item['url'], callback=self.parse_post)
                pass

        next_page = response.xpath("//div[@class='pg']/a[@class='nxt']/@href").extract_first()

        if next_page is not None:
            #yield response.follow(next_page, callback=self.parse_list)
            pass

    def parse_post(self, response):
        post_comment_list = response.xpath("//table[contains(@id, 'pid')]")

        #赞成次数
        print(post_comment_list.xpath(".//span[@id='recommendv_add']/text()").extract_first())
        #反对次数
        print(post_comment_list.xpath(".//span[@id='recommendv_subtract']/text()").extract_first())

        for comment_item in post_comment_list:
            # 楼层信息

            #print(comment_item.xpath(".//div[@class='pi']/strong/a/text()").extract())

            floorNum = comment_item.xpath(".//div[@class='pi']/strong/a/em/text()").extract_first()
            if floorNum is None:
                floorNum = 1
            print(floorNum)

            #postmessage 里面包含了引用信息
            comment_content = comment_item.xpath(".//td[contains(@id, 'postmessage_')]").extract_first()
            #print(comment_content)

            comment_id = comment_item.xpath("..//@id").extract_first()
            print(comment_id)

            comment_poster = comment_item.xpath(".//div[@class='authi']/a/@href").extract_first()
            print(comment_poster)

            poster_id = parse.parse_qs((parse.urlparse(comment_poster)).query).get("uid", [])[0]
            print(poster_id)

            #附件信息
            #图片附件(要考虑需要解析什么附件)
            attachments = comment_item.xpath(".//ignore_js_op/img/@file").extract()
            print(attachments)




        next_page = response.xpath("//div[@class='pg']/a[@class='nxt']/@href").extract_first()
        print(next_page)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_post)
