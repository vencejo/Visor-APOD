#!/usr/python
# -*- coding: utf-8 -*-


import MySQLdb
from gi.repository import Gtk
import os, sys

def creaDb(nombreDB, usuario, password):
    """ Funcion encargada de Crear la base de datos"""
    try:
        conexion = MySQLdb.connect(host='localhost', user='root' ,passwd = password)
        cursor = conexion.cursor()
        query = 'CREATE DATABASE ' + nombreDB
        cursor.execute(query)
        query = 'GRANT ALL ON ' + nombreDB + '.* ' +  'TO ' +  '\'' + usuario + '\'' + '@\'localhost\' ' + 'IDENTIFIED BY ' + '\'' + password +'\'' 
        cursor.execute(query)
        query = 'USE ' + nombreDB
        cursor.execute(query)
        query = """CREATE TABLE Imagenes (id INT NOT NULL AUTO_INCREMENT, Titulo VARCHAR(200),Fecha DATE,Explicacion VARCHAR(4000), Ruta VARCHAR(400),
        Favorita BOOLEAN, PRIMARY KEY (id))"""
        cursor.execute(query)
        conexion.commit()
    except :
        print "Hay un problema con la creacion de la base de datos, puede que ya exista"
        

#--------------------------------------------------
# Clase encargada de gestionar la Base de datos
#--------------------------------------------------

class Db:

    def __init__(self,host,user,passwd,db):

        # Establecemos la conexión
        self.conexion = MySQLdb.connect(host, user,passwd, db)
        # Creamos el cursor
        self.cursor = self.conexion.cursor()
        # Inicializamos la base de datos
        self.initDB()

        
    def initDB(self):
        """ Inicializa la base de datos mediante una llamada a scrapy"""
        
        pass
       
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
