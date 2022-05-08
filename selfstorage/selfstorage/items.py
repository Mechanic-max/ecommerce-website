# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

class SelfstorageItem(scrapy.Item):
    Name = scrapy.Field(
        
    )
    Street = scrapy.Field(
        
    )
    State = scrapy.Field(
        
    )
    Phone = scrapy.Field(
        
    )
    Facility_Amenities = scrapy.Field(
        
    )
    Office_hours = scrapy.Field(
        
    )
    Access_Hours = scrapy.Field(
        
    )
    size = scrapy.Field(
        
    )
    catagory = scrapy.Field(
        
    )
    discount = scrapy.Field(
        
    )
    price = scrapy.Field(
        
    )
    size = scrapy.Field(
        
    )
    description = scrapy.Field(
        
    )
    Size_Catagory_Discount_Price_description = scrapy.Field(
    )
    images_url = scrapy.Field()
    img_url_name = scrapy.Field(
        # output_processor = TakeFirst()
    )
    images = scrapy.Field()
    # def process_item(self, item, spider):
    #     return sorted(Name)

class ListResidentialItem(scrapy.Item):
    image_urls = scrapy.Field()
    img_url_name = scrapy.Field(
        # output_processor = TakeFirst()
    )
    images = scrapy.Field()

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    img_url_name = scrapy.Field(
        # output_processor = TakeFirst()
    )
    images = scrapy.Field()
