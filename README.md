Visor-APOD
==========

Visor de imagenes APOD (Astronomical Picture of the Day) con Python

Este  programa pretende crear un visor offline en un entorno Gtk Linux 
de imagenes descargadas del [sitio oficial APOD de la nasa](http://apod.nasa.gov)

Además se creara un widget asociado que ira mostrando las imagenes en una 
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

Instalación
-----------
Además de los requisitos listados arriba es necesario disponer de un servidor 
[MySQL](http://www.mysql.com/) y un usuario con permisos para la creación de bases de datos (por ejemplo: root).

Para crear la base de datos necesaria sólo hay que ejecutar el siguiente comando:

    $ mysql -u root -p < install/database.sql

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

