# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Tangshi5Item(scrapy.Item):
    father = Field()
    tangshi300 = Field()
    gushi300 = Field()
    songci300=Field()
    shijing = Field()
    yuefu = Field()
    chuci = Field()
    topic = Field()
    title = Field()
    author = Field()
    des = Field()
    url = Field()
    # detail_title = Field()
    # detail_dynasty = Field()
    # detail_text = Field()
    # detail_author = Field()
    # detail_translate_note_text_title = Field()
    # detail_translate_note_url = Field()
    # detail_translate_text_little_title = Field()
    # detail_translate_text = Field()
    # detail_note_text_little_title = Field()
    # detail__note_text = Field()
    # detail_appreciation_background_title = Field()
    # detail_appreciation_url = Field()
    # detail_appreciation_little_title = Field()
    # detail_appreciation_text = Field()
    # detail_background_littlt_title = Field()
    # detail_background_text = Field()
    # detail_background_url = Field()
    pass
