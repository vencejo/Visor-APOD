#!/usr/python
# -*- coding: utf-8 -*-


import MySQLdb
from gi.repository import Gtk
import os, sys
import configobj
import subprocess

#--------------------------------------------------
# Clase encargada de gestionar la configuracion
#--------------------------------------------------    
class Configurador:

    def __init__(self):
                
        self.builder = Gtk.Builder()
        self.builder.add_from_file("configurador.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow ,
                         "iniciarConfiguracion" : self.iniciarConfiguracion,
                         }
        self.builder.connect_signals(self.handlers)
        
        self.VentanaConfiguracion = self.builder.get_object("VentanaConfiguracion")
        
        self.VentanaConfiguracion.show_all()
        
    def creaDb(self, nombreDB, usuario, password):
        """ Funcion encargada de Crear la base de datos"""
        self.conexion = MySQLdb.connect(host='localhost', user='root' ,passwd = password)
        self.cursor = self.conexion.cursor()
        query = 'CREATE DATABASE ' + nombreDB
        self.cursor.execute(query)
        query = 'GRANT ALL ON ' + nombreDB + '.* ' +  'TO ' +  '\'' + usuario + '\'' + '@\'localhost\' ' + 'IDENTIFIED BY ' + '\'' + password +'\'' 
        self.cursor.execute(query)
        query = 'USE ' + nombreDB
        self.cursor.execute(query)
        query = """CREATE TABLE Imagenes (id INT NOT NULL AUTO_INCREMENT, Titulo VARCHAR(200),Fecha DATE,Explicacion VARCHAR(4000), Ruta VARCHAR(400),
        Favorita BOOLEAN, PRIMARY KEY (id))"""
        self.cursor.execute(query)
        self.conexion.commit()
        
    def compruebaDb(self, nombreDB):
        """ Comprueba la creacion de la base de datos , devuelve verdadero si la base de datos se ha creado correctamente """
        query = 'USE ' + nombreDB
        self.cursor.execute(query)
        
        query = "SELECT COUNT(*) FROM Imagenes;"
        self.cursor.execute(query)
        self.conexion.commit()
        registro = self.cursor.fetchone()
        return registro[0] == 0
    
    def iniciarConfiguracion(self, *args):
        
        nombreDB = self.builder.get_object("entry3").get_text()
        usuarioDB = self.builder.get_object("entry6").get_text()
        passwordDB = self.builder.get_object("entry7").get_text()
        
        label = self.builder.get_object("label4")
        
        print nombreDB, usuarioDB, passwordDB
        
        if nombreDB != "" and usuarioDB != "" and passwordDB != "":
            
            self.creaDb(nombreDB, usuarioDB, passwordDB)
        
            #comprueba si la BD se ha creado correctamente, en cuyo caso escribe los datos de acceso a la misma en el archivo de configuracion
            if self.compruebaDb(nombreDB):
                #escribe los datos de la BD en el archivo de configuracion.ini
                config = configobj.ConfigObj()
                config.filename = 'configuracion.ini'
                config["nombreDB"] = nombreDB
                config["usuarioDB"] = usuarioDB
                config["passwordDB"]= passwordDB
                #escribe la ruta de guardado de las imagenes
                config['rutaImagenes'] = os.getcwd()[0:-12] + 'Imagenes' 
                config.write()
                
                #Modifica el archivo settings.py del scrapy para decirle donde tiene que guardar las imagenes
                filename = os.getcwd()[0:-12] + 'APOD_scrapy/APOD_scrapy/settings.py'
                f = open(filename,"r")
                lines = f.readlines()
                f.close()
                f = open(filename,"w")
                for line in lines:
                    if line.find('IMAGES_STORE') == -1:
                        f.write(line)
                f.write('IMAGES_STORE =' + "\"" + config['rutaImagenes'] + "\"")
                f.close()
                
                # oculta el configurador
                self.VentanaConfiguracion.hide()
    
                #Inicio el gestorGUI
                rutaActual = os.getcwd() 
                rutaAGUI= rutaActual[0:-12] + 'GUI'
                os.chdir(rutaAGUI)
                subprocess.call('python gestorGUI.py', shell=True)
                
    def onDeleteWindow(self, *args):
        Gtk.main_quit
        sys.exit()
        
def main():

    app = Configurador()
    Gtk.main()
    return 0
    
if __name__ == '__main__':
    sys.exit(main())


