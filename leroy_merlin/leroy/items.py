# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_price(value):
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        pass
    return value



class LeroyItem(scrapy.Item):
    _id = scrapy.Field(input_processor=MapCompose(get_id), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    parameter_name = scrapy.Field()
    parameter_value = scrapy.Field(input_processor=MapCompose(clean_parameter_value))
    parameters = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(change_price_type), output_processor=TakeFirst())
    images = scrapy.Field()


