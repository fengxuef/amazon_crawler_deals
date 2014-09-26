# -*- coding: utf-8 -*-
#from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.selector import Selector
from ..items import AmazonDealsItem
from datetime import datetime

class DealsSpider(XMLFeedSpider):
    name = 'amazon_deals'
    allowed_domains = ['amazon.com']
    start_urls = ['http://rssfeeds.s3.amazonaws.com/goldbox']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        item = AmazonDealsItem()
        item['title'] = ''.join(node.xpath('title/text()').extract())
        item['link'] = ''.join(node.xpath('link/text()').extract())
        desc_body = ''.join([str(a) for a in node.xpath('description/text()').extract()])
        item['desc'] = desc_body
        #Selector(text=desc_body,type='html').xpath('//text()').extract()
        item['pub_date'] = ''.join(node.xpath('pubDate/text()').extract())
        item['spider_metadata'] = { 'ts': datetime.utcnow(), 'status':'NEW' }
        return item
