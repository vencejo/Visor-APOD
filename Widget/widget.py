##  Programa basado en  magpi_widgets.py 
##  de ColinD
##  para la publicacion MagPi num 8 Noviembre 2012 

import os, Image, Tkinter, pygame, time , glob

# Obtengo informacion sobre las dimensiones de la pantalla y calcula la posicion del widget
t = Tkinter.Tk()
ancho = t.winfo_screenwidth()
baseXPos = int(ancho) - 200 - 10
os.environ['SDL_VIDEO_WINDOW_POS'] = str(baseXPos) + ","+ str(30)

# Ventana sin bordes de pygame que contendra la imagen redimensionada
windowSurface = pygame.display.set_mode((200,200), pygame.NOFRAME)

# Tomo las imagenes de su directorio
rutaActual = os.getcwd() 
rutaAimagenes= rutaActual[0:-6] + 'Imagenes/thumbs/chicas'
os.chdir(rutaAimagenes)
imagenes = glob.glob('*.jpg')

# Se van mostrando las  miniaturas de las imagenes en la esquina superior derecha de la pantalla
for imagen in imagenes:

    imgName = os.path.basename(imagen)
    img = Image.open(imagen)
    imgChica = img.resize((200,200), Image.NEAREST)
    imgChica.save(imgName)
    
    imgCargada = pygame.image.load(imgName)
    windowSurface.blit(imgCargada, (0,0))

    pygame.display.update()

    time.sleep(4)

