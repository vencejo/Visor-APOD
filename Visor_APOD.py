# Programa iniciador de todo

import os, sys, subprocess
from configobj import ConfigObj

if __name__ == '__main__':
    
    rutaActual = os.getcwd() 
    
    # Guarda la ruta actual como ruta raiz de la aplicacion en el archivo configuracion.ini
    
    rutaAconfiguracion = rutaActual + '/Configurador/configuracion.ini'    
    config = ConfigObj(rutaAconfiguracion)
    config['rutaRaiz'] = rutaActual
    config.write()
    
     # Solicito la creacion de la BD si esta es la primera vez que se usa el programa
    if config['porEstrenar'] == 'si':
        #Inicio el configurador
        rutaAconf= rutaActual + '/Configurador/'
        os.chdir(rutaAconf)
        args = [ 'python', 'configurador.py']
        subproceso = subprocess.Popen(args)
        #Espero a que acabe el subproceso
        subproceso.wait()
    
    # Lanza el gestor del GUI
    rutaAGUI= rutaActual+ '/GUI'
    os.chdir(rutaAGUI)
    subprocess.call('python gestorGUI.py', shell=True)
