# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy_mongodb import MongoDBPipeline

class AmazonDealsPipeline(MongoDBPipeline):
    """
    Item pipeline to insert scraped item into mongodb
    """
    def process_item(self, item, spider):
        # the following lines are a duplication of MongoDBPipeline.process_item()
        if self.config['buffer']:
            self.current_item += 1
            item = dict(item)

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = { 'ts': datetime.datetime.utcnow() }

            self.item_buffer.append(item)

            if self.current_item == self.config['buffer']:
                self.current_item = 0
                return self.insert_item(self.item_buffer, spider)
            else:
                return item

        # if the connection exists, don't save it
        matching_item = self.collection.find_one(
            {'link': item['link']}
        )
        if matching_item is not None:
            raise DropItem(
                "Duplicate found for %s, %s" %
                (item['link'], item['link'])
            )
        else:
            return self.insert_item(item, spider)
