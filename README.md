# BattleRoyal-Twitter
Simulacion de unos "Juegos del hambre" en la que pueden participar tantos usuarios de Twitter deseen. 
Utilizando la API de Twitter y Tweepy (la API de Python para conectar la API de Twitter con Python) con varios ficheros en las que
almaceno los datos

# Ficheros:
* inscribirse.py : Programa en la que inicia el plazo de inscripcion para los participantes, funciona comprobando cada X tiempo las menciones que recibe,
si en esas menciones contiene el hashtag GuerrraTwitterxs, si encuentra el hastag copia el nombre del usuario y lo añade al fichero de participantes.
* imagenPresentacion.py : Programa en el que vez estan todos los participantes inscritos sube un tweet con la imagen en la que muestra todos los participantes.
* battleRoyalTW.py : Programa que inicia el juego, basicamente escoge a dos jugadores aleatorios de la lista y los enfrenta, se gana por puro azar.
Por cada victoria obtienes 1 baja, en el cual se comparan las bajas en cada enfrentamiento y el que mas bajas tenga tendra un 15% mas de probabilidades de ganar.
Hay un 10% de posibilidades de resucitar.

# Que he aprendido?
* Familiarizarme con Python, me he introducido en Python para hacer este proyecto, usando un curso en el que te enseñan la base de PYthon.
* API de Twitter, como funciona, que cosas puedo o no puedo hacer con las funciones que ofrecen...
* Tratamiento de datos y ficheros.
