import scrapy


from urllib import parse
from rednet.items import RednetPostItem, RednetPostCommentItem

import re
import execjs

class RednetBbsSpider(scrapy.Spider):
    name = 'rednet_bbs'
    allowed_domains = ['rednet.cn']
    #start_urls = ['']
    clearance = ""

    urls = [
        'https://bbs.rednet.cn/forum.php?mod=forumdisplay&fid=81&filter=author&orderby=dateline',
    ]

    def start_requests(self):

        # yield scrapy.Request("https://bbs.rednet.cn/", callback=self.parse_runjs_cookie)
        # for url in urls:
        #     yield scrapy.Request(url, callback=self.parse_list,
        #                          cookies={#"__jsluid_s": "3901890bc94a6a7843b3857ea32ec485",
        #                                   "__jsl_clearance_s": self.clearance}, dont_filter = True)

        return [scrapy.Request('https://bbs.rednet.cn/', meta={'cookiejar': 1, 'step' : 1}, callback=self.parse_runjs_cookie)]

    def parse(self, response):
        pass

    def parse_runjs_cookie(self, response):
        #print(response.headers) #include set-cookie infos
        #print(response.body)    #include js we need to anlysis

        if response.meta['step'] == 1:
            # 第一次从js中获取clearance
            get_js = re.findall(r'<script>(.*?)</script>', response.body.decode('utf-8'))[0]
            get_js = re.sub('document.cookie=', 'return(', get_js)
            get_js = re.sub(';location.href', ');location.href', get_js)
            get_js = "function getClearance(){" + get_js + "};"
            content = execjs.compile(get_js)
            clearance_temp = content.call('getClearance')
            clearance = (clearance_temp.split(";")[0]).split("=")[-1]
            if clearance is not None:
                self.clearance = clearance
                self.step = 1
                # 第一次获取完毕,组装上set-cookie的信息,进行第二次请求..
                yield scrapy.Request('https://bbs.rednet.cn/', callback=self.parse_runjs_cookie,
                                     meta={'cookiejar': response.meta['cookiejar'], 'step': 2},  # 保证请求链是基于当前请求的cookie
                                     cookies={  # "__jsluid_s": "3901890bc94a6a7843b3857ea32ec485",
                                         "__jsl_clearance_s": self.clearance}, dont_filter=True)
        elif response.meta['step'] == 2:
            get_js = re.findall(r'<script>(.*?)</script>', response.body.decode('utf-8'))[0]  # 去除script
            # 改变函数:从写入cookie到写入全局变量中
            get_js = re.sub(r'document.*?(=.*?)location', r"_clearance\1 return;location", get_js)
            # 修改运行函数
            get_js = get_js.replace("setTimeout", "runNow")
            # 添加运行时环境 nodejs & execjs环境
            get_js = 'const jsdom = require("jsdom");const { JSDOM } = jsdom;const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);window = dom.window;' + get_js
            # 添加变量,函数 javascript
            get_js = "var runNow = function(func, val){func();};var _clearance;var getClearance = function(){return _clearance;};" + get_js

            # 在jsdom的局部环境下运行程序
            ctx = execjs.compile(get_js, cwd=r'E:\project\public_feelings\runtime\node_modules')
            # 调用修改好的程序,获取输出
            clearance_temp = ctx.call("getClearance")
            clearance = (clearance_temp.split(";")[0]).split("=")[-1]
            if clearance is not None:
                self.clearance = clearance
                #正式请求
                yield scrapy.Request(self.urls[0], callback=self.parse_list,
                                     meta={'cookiejar': response.meta['cookiejar']},  # 保证请求链是基于当前请求的cookie
                                     cookies={  # "__jsluid_s": "3901890bc94a6a7843b3857ea32ec485",
                                         "__jsl_clearance_s": self.clearance}, dont_filter=True)


        # yield scrapy.Request(self.urls[0], callback=self.parse_list,
        #                meta={'cookiejar': response.meta['cookiejar'], },  # 保证请求链是基于当前请求的cookie
        #                cookies={  # "__jsluid_s": "3901890bc94a6a7843b3857ea32ec485",
        #                    "__jsl_clearance_s": self.clearance}, dont_filter=True)
        return None

    def parse_list(self, response):

        #print(response.body)  # include js we need to anlysis
        #return None

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
                yield response.follow(post_item['url'], callback=self.parse_post, meta={'cookiejar': 1, 'page': 1})
                pass

        next_page = response.xpath("//div[@class='pg']/a[@class='nxt']/@href").extract_first()

        #帖子列表的下一页
        if next_page is not None:
            #yield response.follow(next_page, callback=self.parse_list, meta={'cookiejar': 1})
            pass

    def parse_post(self, response):
        post_comment_list = response.xpath("//table[contains(@id, 'pid')]")

        print("============================================================================================")
        #print("URL:%s" % response.meta["page"])
        print(response.meta["page"])

        #首个赞成/反对是第一楼的信息
        #赞成次数
        print("帖子点赞:%s" % post_comment_list.xpath(".//span[@id='recommendv_add']/text()").extract_first())
        #反对次数
        print("帖子反对:%s" % post_comment_list.xpath(".//span[@id='recommendv_subtract']/text()").extract_first())

        for comment_item in post_comment_list:
            # 楼层信息

            #print(comment_item.xpath(".//div[@class='pi']/strong/a/text()").extract())

            floorNum = comment_item.xpath(".//div[@class='pi']/strong/a/em/text()").extract_first()
            if floorNum is None:
                floorNum = 1
            print(floorNum)

            agree = comment_item.xpath(".//em/a[@class='replyadd']/span/text()").extract_first()
            if agree is None:
                agree = 0
            subtract = comment_item.xpath(".//em/a[@class='replysubtract']/span/text()").extract_first()
            if subtract is None:
                subtract = 0
            print([agree, subtract])

            #postmessage 里面包含了引用信息，而且可能有关于评论的简评信息
            comment_content = comment_item.xpath(".//td[contains(@id, 'postmessage_')]").extract_first()
            #print(comment_content)

            comment_id = comment_item.xpath("..//@id").extract_first().split("_")[-1]
            print(comment_id)

            comment_poster = comment_item.xpath(".//div[@class='authi']/a/@href").extract_first()
            #print(comment_poster)
            poster_id = parse.parse_qs((parse.urlparse(comment_poster)).query).get("uid", [])[0]
            print(poster_id)

            #附件信息
            #图片附件(要考虑需要解析什么附件)
            attachments = comment_item.xpath(".//ignore_js_op/img/@file").extract()
            print(attachments)


            print("============================================================================================")




        next_page = response.xpath("//div[@class='pg']/a[@class='nxt']/@href").extract_first()
        if next_page is not None:
            print("下一页：" + next_page)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_post, meta={'cookiejar': 1, "page": 1})
