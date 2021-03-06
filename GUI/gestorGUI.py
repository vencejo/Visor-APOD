#!/usr/python
# -*- coding: utf-8 -*-

import MySQLdb
from gi.repository import Gtk
import os, sys, subprocess
from configobj import ConfigObj
import datetime
import signal 

rutaActual = os.getcwd() 
rutaAconfiguracion = rutaActual[0:-3] + 'Configurador/configuracion.ini'
config = ConfigObj(rutaAconfiguracion)

BASEDATOS = config['nombreDB']
USUARIO = config['usuarioDB']
PASSWORD = config['passwordDB']

RUTAIMAGENESGRANDES = config['rutaRaiz']+ "/Imagenes/"
RUTAIMAGENESMEDIANAS = RUTAIMAGENESGRANDES + '/thumbs/medianas/'
RUTADESCRAPY = config['rutaRaiz'] + '/APOD_scrapy'
 
#--------------------------------------------------
# Clase encargada de gestionar la Base de datos
#--------------------------------------------------

class Db:
    
    def __init__(self,host,user,passwd,db):

        # Establecemos la conexión
        self.conexion = MySQLdb.connect(host, user,passwd, db)
        # Creamos el cursor
        self.cursor = self.conexion.cursor()
        # Marcamos el identificador activo
        self.identificador = 1
        
    def get_identificador(self):
        return self.identificador
        
    def set_identificador(self,valor):
        """ Pone el nuevo valor del identificador (id) solo si este esta dentro de los margenes """
        if (0 < valor) and (valor <= self.get_numero_imagenes()):
            self.identificador = valor
        
    def get_numero_imagenes(self):
        """devuelve el numero de imagenes guardadas en la BD"""
        query = "SELECT  COUNT(*) FROM Imagenes ;"
        self.cursor.execute(query)
        self.conexion.commit()
        registro = self.cursor.fetchone()
        
        return int(registro[0])
       
    def deleteDB(self):
        """ Borra todos los registros de la base de datos """

        query= "DELETE FROM Imagenes WHERE 1;"
        self.cursor.execute(query)
        self.conexion.commit()


    def obtener(self, identificador):
        """ Devuelve el registro de la tabla con el identificador dado, si el id no existe devuelve None """

        query = "SELECT * FROM Imagenes WHERE id = {0} ;".format(str(identificador))

        self.cursor.execute(query)
        self.conexion.commit()
        registro = self.cursor.fetchone()
        return registro
             
    def marcaFavorita(self,identificador, esFavorita):
        """ Marca como favorita un id si la variable "esFavorita" es True y lo desmarca si "esFavorita" es falso"""

        if esFavorita:
            favorita = 'TRUE'
        else:
            favorita = 'FALSE'
            
        query = "UPDATE Imagenes SET Favorita = {0} WHERE id = {1} ;".format(favorita,str(identificador))
        self.cursor.execute(query)
        self.conexion.commit()
        
#--------------------------------------------------
# Clase encargada de gestionar la interfaz grafica
#--------------------------------------------------    
class GUI:

    def __init__(self):
                
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow ,
                         "onNuevaDB": self.onNuevaDB,
                         "onOpenAbout": self.onOpenAbout,
                         "onCloseAbout": self.onCloseAbout,
                         "onAdelanteClick" : self.onAdelanteClick,
                         "onAtrasClick" : self.onAtrasClick,
                         "onFavoritaClick" : self.onFavoritaClick,
                         "initDBconScrapy_Mes" : self.initDBconScrapy_Mes,
                         "initDBconScrapy_Year" : self.initDBconScrapy_Year,
                         "initDBconScrapy_Todo" : self.initDBconScrapy_Todo,
                         "onImagenClick" : self.mostrarImagenGrande,
                         "onCloseImagenGrande" : self.onCloseImagenGrande, 
                         "editarConGimp" : self.editarConGimp,
                         "onIniciarWidget" : self.onIniciarWidget,
                         "onPararWidget": self. onPararWidget,
                         }
        self.builder.connect_signals(self.handlers)
        
        self.window = self.builder.get_object("window1")
        self.ventanaImagenGrande = self.builder.get_object("dialog1")
        self.ventanaImagenGrande.hide()
        self.spinner = self.builder.get_object("spinner1")
        self.imagenesDescargadas = False
        self.rutaImagen = ""
        self.procesoWidget = 0
        
        # Mostramos la pantalla inicial
        self.pantallaInicial()
        
        #Conectamos a la BD
        self.tabla = Db(host='localhost', user=USUARIO,passwd=PASSWORD, db=BASEDATOS)
        
        self.window.show_all()
        self.spinner.hide()
        
    def onNuevaDB(self, *args):
         #Inicio el configurador
        rutaActual = os.getcwd() 
        rutaAconf= rutaActual[0:-3] + 'Configurador'
        os.chdir(rutaAconf)
        args = [ 'python', 'configurador.py']
        subproceso = subprocess.Popen(args)
        #Espero a que acabe el subproceso
        subproceso.wait()
    
    def calculaMesyYear(self):
        """Calcula el mes y año actuales y los pasa a una tupla con cadenas """
        fechaActual = datetime.date.today().__str__()
        mes = fechaActual[5:7]
        year = fechaActual[2:4]
        
        return (mes, year)
        
    def initDBconScrapy_Mes(self, *args):
        """ Prepara todo para la descarga de imagenes del mes actual con Scrapy """
        mes, year = self.calculaMesyYear()
        config['year'] =  year
        config['mes'] = mes
        config.write()
        self.initDBconScrapy()
 
    def initDBconScrapy_Year(self, *args):
        """ Prepara todo para la descarga de imagenes del año actual con Scrapy """
        mes, year = self.calculaMesyYear()
        config['year'] = year
        config['mes'] = ''
        config.write()
        self.initDBconScrapy()
        
    def initDBconScrapy_Todo(self, *args):
        """ Prepara todo para la descarga de imagenes de todos los años con Scrapy """
        config['year'] = ''
        config['mes'] = ''
        config.write()
        self.initDBconScrapy()
        
    def initDBconScrapy(self):
        """ Inicializa la base de datos mediante una llamada a scrapy que descarga los datos de la web y los vuelca en la BD"""
        
        if not self.imagenesDescargadas :
            
             # Aviso del inicio de la descarga
            self.imagenesDescargadas = True
            self.spinner.show()
            self.spinner.start()
            statusBar = self.builder.get_object("statusbar1")
            context_id = statusBar.get_context_id("aviso")
            statusBar.pop(context_id)
            statusBar.push(context_id, "Realizando  la descarga, espere por favor")
            self.window.show_all()
            statusBar.show()
               
            # Comienza el proceso de descarga en si
            os.chdir(RUTADESCRAPY)
            subprocess.call('scrapy crawl APOD_scrapySpider', shell=True)
            
            # Aviso del fin de la descarga
            statusBar.pop(context_id)
            statusBar.push(context_id, "Imagenes correctamente descargadas, ya puede empezar la visualizacion")
            statusBar.show()
            self.spinner.stop()
            self.spinner.hide()

    def pantallaInicial(self):
        """ Muestra la pantalla inicial de bienvenida en el visor """
        image = self.builder.get_object("image1")
       
        textview = self.builder.get_object("textview1")
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        explicacion = textview.get_buffer()
        textoInicio = """ Si no lo has echo ya o  si quieres crear una nueva Base de Datos para las imagenes pincha en 
        configurarDB y sigue las instrucciones. Ten en cuenta que para que funcione hay que tener instaldado MySQL  
        
        Tras esto ya podemos comenzar con el proceso de descarga de las imagenes, para lo cual 
        hay que hacer Archivo -> Iniciar descarga lo que pondra a trabajar a Scrapy bajando las imagenes.
        Este proceso de descarga solo hay que hacerlo la primera vez que abrimos el gestorGUI, una vez por cada base de datos.
        Se informa con un mensaje en la barra de estado cuando Scrapy acaba de descargarlas. 
        
        Es entonces cuando podemos empezar a ver las imagenes pulsando en los botones Adelante y Atras. 
        Marcarlas como favoritas, verlas en tamaño grande o editarlas con Gimp. """
        explicacion.set_text(textoInicio)
        image.set_from_file('portada.jpg')
        self.window.show_all()
        
    def poblarItemsGUI(self, registro):
        """Rellena los campos del GUI con los datos del registro """
        
        #Obtengo los objetos del GUI  
        image = self.builder.get_object("image1")
        titulo = self.builder.get_object("entry1")
        fecha = self.builder.get_object("entry2")
        textview = self.builder.get_object("textview1")
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        explicacion = textview.get_buffer()
        ident = self.builder.get_object("entry4")
        favorita = self.builder.get_object("entry5")
        
        #Relleno los objetos del GUI con los datos del registro
        ident.set_text(str(registro[0]) +  " de " + str(self.tabla.get_numero_imagenes()))
        titulo.set_text(str(registro[1]))
        fecha.set_text(str(registro[2]))
        texto_plano = str(registro[3])
        explicacion.set_text(texto_plano)
        if str(registro[5]) == '0':
            favorita.set_text('No lo es')
        else:
            favorita.set_text('Lo es')
            
        self.rutaImagen = str(registro[4])
        ruta =  RUTAIMAGENESMEDIANAS + self.rutaImagen[4:]
        image.set_from_file(ruta)
        
    def onAdelanteClick(self, *args):
        """Al pulsar en el boton adelante avanzamos en la BD """
        #Aumento el id de la tabla de la BD
        ident = self.tabla.get_identificador()
        self.tabla.set_identificador(ident + 1)
        #Consultamos la BD
        registro = self.tabla.obtener(self.tabla.get_identificador())
        #actualizo el GUI con los datos
        self.poblarItemsGUI(registro)
        
    def onAtrasClick(self, *args):
        """Al pulsar en el boton atras retrocedemos en la BD """
        #Aumento el id de la tabla de la BD
        ident = self.tabla.get_identificador()
        self.tabla.set_identificador(ident - 1)
        #Consultamos la BD
        registro = self.tabla.obtener(self.tabla.get_identificador())
        #actualizo el GUI con los datos
        self.poblarItemsGUI(registro)
        
    def onFavoritaClick(self, *args):
        """Marca una imagen como favorita si no lo es y la desmarca en caso contrario"""
        favorita = self.builder.get_object("entry5")
        
        if favorita.get_text() == 'No lo es':
            self.tabla.marcaFavorita(self.tabla.get_identificador(), True)
            favorita.set_text('Lo es')
        else:
            self.tabla.marcaFavorita(self.tabla.get_identificador(), False)
            favorita.set_text('No lo es')
            
    def mostrarImagenGrande(self, *args):
        
        if self.rutaImagen:
            imagenGrande = self.builder.get_object("imagenGrande")
            ruta =  RUTAIMAGENESGRANDES + self.rutaImagen 
            imagenGrande.set_from_file(ruta)
            self.ventanaImagenGrande.show_all()
            
    def onCloseImagenGrande(self, *args):
        self.ventanaImagenGrande.hide()
        
    def editarConGimp(self, *args):
        
        if self.rutaImagen:
            ruta =  RUTAIMAGENESGRANDES + self.rutaImagen
            subprocess.Popen(['gimp', ruta])
            
    def onIniciarWidget(self, *args):
        #Inicio el widget
        rutaActual = os.getcwd() 
        rutaAwidget= config['rutaRaiz'] + '/Widget'
        os.chdir(rutaAwidget)
        self.procesoWidget = subprocess.Popen(['python','widget.py'],stdin=subprocess.PIPE)
        
    def onPararWidget(self, *args):
        self.procesoWidget.kill()
        
        
    def onDeleteWindow(self, *args):
        Gtk.main_quit
        sys.exit()
        
    def onOpenAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.show_all()

    def onCloseAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.hide()

    
def main():
    
    app = GUI()
    Gtk.main()
    return 0
    
if __name__ == '__main__':
    sys.exit(main())

