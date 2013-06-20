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

import sys, os
import MySQLdb
import hashlib
import re
from configobj import ConfigObj

rutaActual = os.getcwd() 

rutaAconfiguracion = rutaActual[0:-12] + '/GUI/configuracion.ini'
print ""
print rutaAconfiguracion
print ""

config = ConfigObj(rutaAconfiguracion)

usuario = str(config['usuarioDB'])
password = str(config['passwordDB'])
dataBase = str(config['nombreDB'])

class guardadoSQLPipeline(object):
    
    def __init__(self):
        self.conn =  MySQLdb.connect(host='localhost', user=usuario,passwd=password, db=dataBase, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
    
    def process_item(self, item, spider):  
    
        # La cadena de la fecha se transforma al formato SQL (YYYY-MM-DD)
        fecha = self.adaptarFecha(item['fecha'])
        texto = self.htmlAtexto(item['explicacion'])
        try:
            self.cursor.execute("""INSERT INTO Imagenes (Titulo, Fecha, Explicacion, Ruta, Favorita)  
                            VALUES (%s, %s,%s, %s,%s)""", 
                           (item['titulo'], 
                            fecha,
                            texto,
                            item['image_paths'][0],
                            'FALSE'))

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item
        
    def adaptarFecha(self, fecha):
        """ transforma una fecha del tipo '2013 June 26' en '2013-06-26' que es el formato oficial MySQL """
        (year, month, day) = fecha.split()
        
        listaMeses = ['January','February','March','April','May','June','July','August','September','October','November','December']
    
        month = listaMeses.index(month) + 1
        
        return year + '-' + str(month) + '-' + day    
        
    def htmlAtexto(self, data):       
        """Funcion auxiliar para transformar un texto html en otro plano si etiquetas """
        # borra los saltos de linea
        data = data.replace("\n", " ")
       
        # borra todas las etiquetas html
        p = re.compile(r'<[^<]*?>')
        data = p.sub('', data)
      
        return data
        
    
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

