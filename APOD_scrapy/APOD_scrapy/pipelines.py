# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class guardadoXMLPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):

        # fichero de guardado
        self.file = open('datos.xml', 'w+b')

        self.exporter = XmlItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
    
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        """Solo procesa las imagenes y se deshace de las referencias a los videos """
        if item['ruta_imagen']:
            self.exporter.export_item(item)
            return item
        else:
            raise DropItem("Este dia no hay imagen  %s" % item)


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """Solo descarga las imagenes y se deshace de las referencias a los videos """
        if item['image_urls']:
            for image_url in item['image_urls']:
                yield Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

