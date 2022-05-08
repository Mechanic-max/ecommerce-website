# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from os import path


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        name = request.meta['name']
        # return 'images/' + os.path.basename(urlparse(request.url).path)
        ex = os.path.basename(urlparse(request.url).path).split('.')[-1]
        return 'images/' + name + '.' + ex

    def get_media_requests(self, item, info):
        for i, images_url in enumerate(item['images_url']):
            meta = {}
            meta['name'] = item['img_url_name'][i]
            yield scrapy.Request(images_url, meta=meta)

    def image_key(self, url):
        image_guid = url.split('/')[-1]
        return 'full/%s' % (image_guid)

    # def image_downloaded(self, response, request, info):
    #     checksum = None
    #     for path, image, buf in self.get_images(response, request, info):
    #         if checksum is None:
    #             buf.seek(0)
    #             checksum = md5sum(buf)
    #         width, height = image.size
    #         path = 'full/%s' % img_url_name
    #         self.store.persist_file(
    #             path, buf, info,
    #             meta={'width': width, 'height': height},
    #             headers={'Content-Type': 'image/jpeg'})
    #     return checksum