# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from APOD_scrapy.items import ApodScrapyItem
from configobj import ConfigObj
import os

def creaCadenaDeConsulta():
        
        rutaActual = os.getcwd() 
        rutaAconfiguracion = rutaActual[0:-12] + '/Configurador/configuracion.ini'
        config = ConfigObj(rutaAconfiguracion)

        mes = str(config['mes'])
        year = str(config['year'])
        
        if mes == '' and year == '':
            cadena = r'/apod/ap\d+\.html'
        elif mes == '' and year != '':
            cadena = r'/apod/ap' + year + '\d+\.html'
        elif mes != '' and year != '':
            cadena = r'/apod/ap' + year + mes + '\d\d\.html'
        else:
            "Configuracion de mes y año erronea "
        
        return cadena
        
class APOD_scrapySpider(CrawlSpider):
    name = 'APOD_scrapySpider'
    start_urls = ['http://apod.nasa.gov'] # url de inicio de busqueda para la spider

    # Analiza solo los post con estructura r'^ap\d{6}'  r'/apod/ap\130619\.html' r'/apod/ap\d+\.html'
    rules = (Rule(SgmlLinkExtractor(allow=[creaCadenaDeConsulta()]),callback='analizaEntrada',follow= True) ,
    )           

    def analizaEntrada(self, response):

        hxs = HtmlXPathSelector(response)
        item = ApodScrapyItem()

        item['titulo'] = (hxs.select('//html/body/center[2]/b[1]/text()').extract()[0]).encode("utf-8")
        item['fecha'] = ((hxs.select("//html/body/center/p[2][1]/text()").extract()[0]).replace("\n","")).encode("utf-8")
        item['explicacion'] = (hxs.select("//html/body/p[1]").extract()[0]).encode("utf-8")
        item['ruta_imagen'] = (hxs.select("//html/body/center/p[2]/a[1]/img/@src")).extract()
        if item['ruta_imagen']:
            enlace_a_imagen = ('http://apod.nasa.gov/apod/' + item['ruta_imagen'][0]).encode("utf-8")
            item['image_urls'] = [enlace_a_imagen]
        else:
            item['image_urls'] = []
    
        return item
        
    
        
        
        
