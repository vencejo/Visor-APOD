Visor-APOD
==========

Visor de imágenes APOD (Astronomical Picture of the Day) con Python

Este  programa pretende crear un visor offline en un entorno Gtk Linux 
de imágenes descargadas del [sitio oficial APOD de la nasa](http://apod.nasa.gov)

Además se creara un widget asociado que ira mostrando las imágenes favoritas en una 
pequeña porción de la pantalla 

Es mi Proyecto para el **Curso de Programación
Avanzada en Python, 2ª Edición** del [Centro de Enseñanzas Virtuales de la
Universidad de Granada](http://cevug.ugr.es), y su objetivo es poner en práctica
algunas de las técnicas aprendidas.


Requisitos
----------
* [Python 2.7](http://www.python.org/)
* [Pygame](http://www.pygame.org)
* [MySQLdb](http://sourceforge.net/projects/mysql-python/)
* [Scrapy](https://scrapy.org/)
* [configObj](http://www.voidspace.org.uk/python/configobj.html)

Instalación
-----------
Además de los requisitos listados arriba es necesario disponer de un servidor 
[MySQL](http://www.mysql.com/) y un usuario con permisos para la creación de bases de datos (por ejemplo: root).

Funcionamiento
-----------
Iniciamos  el programa yendo  a la raiz de la carpeta donde se tenga descargado y pinchando en Visor-APOD.py que abrirá
la ventana principal.

Para crear la base de datos necesaria y configurar las carpetas de descarga solo hay que pinchar en configurarDB
en la ventana del programa y rellenar los datos que se piden , en la contraseña hay que poner la del acceso al entorno mySQL.
El configurador se encarga de crear la base de datos y de fijar las carpetas de destino de las imágenes dentro de la carpeta Imágenes.

Una vez hecho esto , para poder empezar a trabajar con el visor
lo primero que hay que hacer es comenzar con el proceso de descarga de las imágenes, para lo cual hay que hacer 
Archivo -> Iniciar descarga lo que pondrá a trabajar a Scrapy bajando las imágenes. 
Se puede elegir si descargar las imagenes del mes actual, o del año actual o de todo el archivo APOD.

Este proceso de descarga solo hay que hacerlo la primera vez que abrimos el gestorGUI, una vez por cada base de datos.

Se informa con un mensaje en la barra de estado cuando Scrapy acaba de descargarlas. Es entonces cuando podemos empezar a ver
las imágenes pulsando en los botones Adelante y Atrás. Marcarlas como favoritas, verlas en tamaño grande o editarlas con Gimp. 

Espacio y Paciencia
-----
Si eliges descargar todas las imágenes APOD tienes que armarte de espacio (tener al menos 1GB libre) y paciencia 
(todas las imágenes (~ 7000) tardan en descargarse en torno a la media hora en una conexión rápida) 

Nota sobre la implementación
-----------
Los diferentes scripts se comunican entre si mediante el archivo configuracion.ini. 
Así configurador.py se encarga de generarlo y es consultado tanto por el gestorGUI como 
por Scrapy para ver donde coger o dejar las imágenes y los parámetros de la Base de Datos.

Errores detectados
-----

Posibles mejoras
-----

To-Do
-----
[Tareas pendientes](https://github.com/vencejo/Visor-APOD/issues?state=open)

Créditos
--------
- [APOD en la Wikipedia](https://en.wikipedia.org/wiki/Astronomy_Picture_of_the_Day)

Licencia
--------

Diego J. Martinez García - apussapus@gmail.com - [guadatech](http://guadatech.blogspot.com.es/)

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES"><img alt="Licencia de Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />
Este obra está bajo una <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES">licencia de Creative Commons Reconocimiento 3.0 Unported</a>.
