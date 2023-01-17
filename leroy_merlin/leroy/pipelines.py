# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import re
import os

class LeroyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy


    def process_item(self, item, spider):
        return item


class LeroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for image_page_link in item['images']:
                yield scrapy.Request(image_page_link)
        else:
            print(f'{item["_id"]} has no images')

    def file_path(self, request, response=None, info=None):
        pattern = re.compile('\/(\d+)')
        product_id = re.findall(pattern, request.url)[0]
        dir_path = f'{os.getcwd()}\\images\\{product_id}\\'
        file_name = os.path.basename(request.url)
        file_path = f'{dir_path}{file_name}'
        return file_path






    def item_completed(self, results, item, info):
        
        if results[0]:
            item['images'] = [image_tuple[1] for image_tuple in results if image_tuple[0]]
        return item