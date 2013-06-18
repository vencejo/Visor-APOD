# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApodScrapyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    
    titulo = Field()
    fecha = Field()
    explicacion = Field()
    tipo = Field()
    ruta_imagen = Field()
    ruta_local = Field()
    dimension_x = Field()
    dimension_y = Field()
    peso = Field()
    favorito = Field()
    
    image_urls = Field()
    images = Field()
    image_paths = Field()
