# Programa iniciador de todo

import os, sys, subprocess

if __name__ == '__main__':
    
    rutaActual = os.getcwd() 
    rutaAGUI= rutaActual+ '/GUI'
    os.chdir(rutaAGUI)
    subprocess.call('python gestorGUI.py', shell=True)
