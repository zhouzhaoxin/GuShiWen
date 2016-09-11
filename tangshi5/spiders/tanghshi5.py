# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from tangshi5.items import Tangshi5Item
from scrapy.spiders import Spider
from scrapy.http import HtmlResponse
import requests
import re


class Tanghshi5Spider(Spider):
    name = "tangshi5"
    allowed_domains = ["gushiwen.org"]
    start_urls = [
        "http://so.gushiwen.org/gushi/tangshi.aspx"
        # "http://so.gushiwen.org/gushi/sanbai.aspx",
        # "http://so.gushiwen.org/gushi/songsan.aspx",
        #诗经有问题
        # "http://so.gushiwen.org/gushi/shijing.aspx"
        # "http://so.gushiwen.org/gushi/yuefu.aspx",
        # "http://so.gushiwen.org/gushi/chuci.aspx"
    ]

    def __init__(self):
        self.site_domain = 'http://so.gushiwen.org'
        self.items = []
        self.item_father = []
        self.item = Tangshi5Item()

        self.itemin_topic=[]
        self.item_result = {}
        self.numb = 0


    def parse(self, response):
        print(type(response))
        sel = Selector(response)
        sites1 = sel.xpath('//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]')
        sites = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"五言绝句：")]/parent::div')
        sites2 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"七言绝句：")]/parent::div')

        sites3 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"五言律诗：")]/parent::div')
        # 问题
        sites4 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"七言律诗：")]/parent::div')
        #作者没有
        sites5 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"五言古诗：")]/parent::div')

        sites6 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"七言古诗：")]/parent::div')

        sites7 = sel.xpath(
            u'//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"乐府：")]/parent::div')

        for site in sites1:
            topic = site.xpath('span[@style]/text()').extract()
            # author = site.xpath('span[not(@style)]/text()').extract()

            for top in topic:
                itemi_topic={}
                test_title_str = top.encode('utf-8')
                print(test_title_str)
                itemi_topic['topic'] = test_title_str
                test_title_str = test_title_str.decode('utf-8')
                test_title_temp_1 ='//body/div[@class="main3"]/div[@class="leftlei"]/div[@class="son2"]/span[contains(text(),"%s")]/parent::div'%test_title_str
                sites8 = sel.xpath(test_title_temp_1)
                title = sites8.xpath('span[not(@style)]/a/text()').extract()
                url = sites8.xpath('span[not(@style)]/a/@href').extract()
                itemin = []
                for itemindex in range(len(title)):
                    itemi = {}
                    itemi['title'] = title[itemindex].encode('utf-8')
                    # itemi['author'] = author[itemindex].encode('utf-8')
                    itemi['url'] = self.site_domain + url[itemindex].encode('utf-8')
                    #处理细节
                    self.handle_detail(itemi['url'], itemi)
                    itemin.append(itemi)

                itemi_topic['des'] = itemin
                self.itemin_topic.append(itemi_topic)
        self.item['chuci'] = self.itemin_topic
        self.items.append(self.item)
        return self.items

    def handle_detail(self, response, itemi):
        print(response)
        response = response.strip()
        # requests.adapters.DEFAULT_RETRIES = 10
        # s = requests.session()
        # s.config['keep_alive'] = False
        html_requests_item = requests.get(response)
        html_requests = html_requests_item.text.encode('utf-8')
        # html_requests_item.connection.close()

        html_response = HtmlResponse(url=response, body=html_requests, headers={'Connection': 'close'})
        html_all = Selector(html_response)
        html = html_all.xpath('//div[@class="main3"]/div[@class="shileft"]')
        itemi['detail_dynasty'] = html.xpath(
            u'div[@class="son2"]/p/span[contains(text(),"朝代：")]/parent::p/text()').extract()[0]
        itemi['detail_translate_note_url'] = html.xpath(
            u'div[@class="son5"]//u[contains(text(),"译文及注释")]/parent::a/@href').extract()

        itemi['detail_appreciation_url'] = html.xpath(
            u'div[@class="son5"]//u[contains(text(),"赏")]/parent::a/@href').extract()

        itemi['detail_background_url'] = html.xpath(
            u'div[@class="son5"]//u[contains(text(),"诗的故事") or contains(text(),"创作背景")]/parent::a/@href').extract()
        itemi['detail_author'] = html.xpath(
            u'div[@class="son2"]/p/span[contains(text(),"作者：")]/parent::p/a/text()').extract()

        itemi['detail_text'] = "".join(html.xpath('div[@class="son2"]/text()').extract()).strip().encode('utf-8')
        # itemi['detail_text'] = re.sub(r'：',"“",itemi['detail_text'])
        # itemi['detail_text'] = re.sub(r'\(.*?\)',"",itemi['detail_text'])
        itemi['detail_text'] = re.sub(r'\r?\n\t?.*?\)', "", itemi['detail_text'])

        if itemi['detail_background_url']:
            self.detail_background(itemi['detail_background_url'], itemi)
            pass
        else:
            pass

        self.detail_translate_note(itemi['detail_translate_note_url'], itemi)
        self.detail_appreciation(itemi['detail_appreciation_url'], itemi)

    # 处理诗歌背景
    def detail_background(self, all_url, itemi):
        detail_appreciation_container = []
        for url in all_url:
            url = self.site_domain + url
            print('detail_background_text url : %s' % url)
            html_requests = requests.get(url).text.encode('utf-8')
            html_response = HtmlResponse(url=url, body=html_requests, headers={'Connection': 'close'})
            html_all = Selector(html_response)
            temp = ''.join(html_all.xpath(
                u'//div[@class="main3"]/div[@class="shileft"]/div[@class="shangxicont"]/p[not(@style or contains(text(),"参考资料："))]').extract())
            temp = temp.encode('utf-8')
            temp = re.sub(r'<p>', '', temp)
            temp = re.sub(r'</p>', '', temp)
            temp = re.sub(r'</a>', '', temp)
            temp = re.sub(r'(<a\s+href=\s*\".*?\">)', '', temp)
            alt = re.search(r'\s+alt=\s*\"(.*?)\"\s+', temp)
            # print(alt.group(1))
            if alt is not None:
                temp = re.sub(r'<img.*\s*>', alt.group(1), temp)
            else:
                print('%s have a none img' % url)
            temp = re.sub(r'\"', "“", temp)

            detail_appreciation_container.append(temp)
        itemi['detail_background_text'] = detail_appreciation_container

    # 处理译文及注释
    def detail_translate_note(self, all_url, itemi):
        for url in all_url:
            url = self.site_domain + url
            print('detail_translate_note url %s' % url)
            html_requests = requests.get(url).text.encode('utf-8')
            html_response = HtmlResponse(url=url, body=html_requests, headers={'Connection': 'close'})
            html_all = Selector(html_response)
            itemi['detail_translate_note_text_title'] = html_all.xpath(
                '//div[@class="main3"]/div[@class="shileft"]/div[@class="son1"]/h1/text()').extract()
            itemi['detail_translate_text'] = html_all.xpath(
                '//div[@class="main3"]/div[@class="shileft"]/div[@class="shangxicont"]/p[not(@style)]/descendant-or-self::text()').extract()
            item_list_temp = []
            for item_list in itemi['detail_translate_text']:
                temp = item_list.encode('utf-8')
                temp = re.sub(r'\"', "“", temp)
                item_list_temp.append(temp)
            itemi['detail_translate_text'] = item_list_temp
        pass

    # 处理赏析
    def detail_appreciation(self, all_url, itemi):
        detail_appreciation_container = []
        for url in all_url:
            url = self.site_domain + url
            print('detail_appreciation url : %s' % url)
            html_requests = requests.get(url).text.encode('utf-8')
            html_response = HtmlResponse(url=url, body=html_requests, headers={'Connection': 'close'})
            html_all = Selector(html_response)
            temp = ''.join(html_all.xpath(
                u'//div[@class="main3"]/div[@class="shileft"]/div[@class="shangxicont"]/p[not(@style or contains(text(),"参考资料："))]').extract())
            temp = temp.encode('utf-8')
            temp = re.sub(r'<p>', '', temp)
            temp = re.sub(r'</p>', '', temp)
            temp = re.sub(r'</a>', '', temp)
            temp = re.sub(r'(<a\s+href=\s*\".*?\">)', '', temp)
            alt = re.search(r'\s+alt=\s*\"(.*?)\"\s+', temp)
            # print(alt.group(1))
            if alt is not None:
                temp = re.sub(r'<img.*\s*>', alt.group(1), temp)
            else:
                print('%s have a none img in appricate' % url)
            temp = re.sub(r'\"', "“", temp)
            # if self.site_domain + '/shangxi_4618.aspx' == url:
            # print(temp)
            detail_appreciation_container.append(temp)
        itemi['detail_appreciation_text'] = detail_appreciation_container
        pass