# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy import Request
import json
from image360.items import Image360Item
class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = Image360Item()
            item['id'] = image.get('imageid')
            item['title'] = image.get('group_title')
            item['url'] = image.get('qhimg_url')
            yield item

    def start_requests(self):
        data = {
            'ch':'photography',
            'liststyle':'new',
            'temp':'1'
        }
        base_url = 'https://image.so.com/zj?'
        for page in range(1,10):
            data['page'] = page * 30
            param = urlencode(data)
            url = base_url + param
            yield Request(url = url,callback=self.parse)