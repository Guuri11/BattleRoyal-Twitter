import tweepy
import time
from PIL import Image, ImageFont, ImageDraw
import random

CONSUMER_KEY = # SECRET KEY FROM TWTTER API
CONSUMER_SECRET = # SECRET KEY FROM TWTTER API
ACCESS_KEY = # SECRET KEY FROM TWTTER API
ACCESS_SECRET = # SECRET KEY FROM TWTTER API


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# FUNCIONES LISTAS
def obtenerListaJugadores(): # DE VUELVE LOS DATOS DEL FICHERO A UNA LISTA (returns players' list)
    lista = []
    fichero = open('listaJugadores.txt','r')
    for linea in fichero:
        linea = linea.rstrip("\n")
        lista.append(linea)
    fichero.close()
    return lista

def getListaBajas():    # DE VUELVE LOS DATOS DE LAS BAJAS (returns kills' list)
    bajas = open('bajas.txt','r')
    lista=[]
    for linea in bajas:
        linea = linea.rstrip("\n")
        lista.append(linea)
    bajas.close()
    return lista

def actualizarBajas(listaBajas, ganador): # update kills
    for linea in range(len(listaBajas)):
        if linea == ganador:
            listaBajas[linea] = int(listaBajas[linea])
            listaBajas[linea] +=1
            fichero = open('bajas.txt','w')
            for linea in range(len(listaBajas)):
                fichero.write(str(listaBajas[linea])+'\n')
            fichero.close()

    return listaBajas

def getEliminados(): # get kills
    listaEliminados = []
    fichero = open('eliminados.txt','r')
    for linea in fichero:
        linea = linea.rstrip("\n")
        listaEliminados.append(linea)
    fichero.close()
    return listaEliminados

# FUNCIONES DE IMAGEN
imagen = Image.new('RGBA',(1400,1200),'white')  #imagen donde cargar los nombres
font = ImageFont.truetype('arial.ttf',30,0,'utf-8',None)    # tipo de fuente
draw = ImageDraw.Draw(imagen) # objeto para dibujar sobre la imagen los nombre
x = 50  # posicion X
y = 50  # posicion Y

def dibujarTablero(x,y,lista): # draw the image where displays the players' names for the first time
    for i in range(len(lista)):
        if y == 1100:
            nombre = lista[i]
            draw.text((x,y),nombre,font=font,fill='black')
            y = 50
            x +=280
        else:
            nombre = lista[i]
            draw.text((x,y),nombre,font=font,fill='black')
            y+=50

def actualizarTablero(x,y,lista,listaEliminados): # update the image showing who is dead or not
    for i in range(len(lista)):
        if y == 1100:
            nombre = lista[i]
            draw.text((x,y),nombre,font=font,fill='black')
            for i in range(len(listaEliminados)):
                if listaEliminados[i] == nombre:
                    draw.text((x,y),nombre,font=font,fill='red')
                    break
            y = 50
            x +=280
        else:
            nombre = lista[i]
            draw.text((x,y),nombre,font=font,fill='black')
            for i in range(len(listaEliminados)):
                if listaEliminados[i] == nombre:
                    draw.text((x,y),nombre,font=font,fill='red')
                    break
            y+=50

# FUNCIONES DE ENFRENTAMIENTOS
def duelo(listaJugadores,listaEliminados, listaBajas): # function that battles two players and returns the result
    jugadores = escogerJugadores(listaJugadores,listaEliminados)
    resultado = enfrentarJugadores(listaJugadores, jugadores, listaBajas, listaEliminados)
    return resultado
def escogerJugadores(listaJugadores,listaEliminados):   # chose which two players will fight
    jugador1 = None
    while jugador1 == None:
        jugador1 = int(random.random()*len(listaJugadores))
        for idx in range(len(listaEliminados)):
            if listaJugadores[jugador1] == listaEliminados[idx]:
                jugador1 = None
                break
    jugador2 = None
    while jugador2 == None or jugador2 == jugador1:
        jugador2 = int(random.random()*len(listaJugadores))
        for idx in range(len(listaEliminados)):
            if listaJugadores[jugador2] == listaEliminados[idx]:
                jugador2 = None
                break
    return [jugador1,jugador2]

def enfrentarJugadores(listaJugadores, jugadores, listaBajas, listaEliminados): # Fight between the players
    jugador1 = listaJugadores[jugadores[0]] #Almaceno el nombre del jugador
    jugador2 = listaJugadores[jugadores[1]]
    bajas1 = listaBajas[jugadores[0]]   #Almaceno bajas correspondientes de cada jugador
    bajas2 = listaBajas[jugadores[1]]
    res = int(random.random()*100)  # Loteria para enfrentamiento
    if bajas1 > bajas2:
        if (res >=50 and res <=65) or res%2 ==0:
            ganador = jugadores[0]
            perdedor = jugadores[1]
        else:
            ganador = jugadores[1]
            perdedor = jugadores[0]
    elif bajas2> bajas1:
        if (res >=50 and res <=65) or res%2 ==0:
            ganador = jugadores[1]
            perdedor = jugadores[0]
        else:
            ganador = jugadores[0]
            perdedor = jugadores[1]
    else:
        if res%2 == 0:
            ganador = jugadores[0]
            perdedor = jugadores[1]
        else:
            ganador = jugadores[1]
            perdedor = jugadores[0]
    return [ganador, perdedor,jugador1,jugador2]

def resucitar(listaEliminados): # function that revives a player
    lista = listaEliminados
    ran = int(random.random()*len(listaEliminados))
    print('Ha resucitado',listaEliminados[ran])
    resucitado = lista[ran]
    del lista[ran]
    actualizarTablero(x,y,listaJugadores,listaEliminados)
    imagen.save("im.png")
    ran = random.randint(1,3)
    if ran == 1:
        api.update_with_media('im.png',("Ou mama... @"+resucitado+" ha vuelto para vengarse"))
    elif ran == 2:
        api.update_with_media('im.png',("Ha resurgido de las cenizas @"+resucitado))
    elif ran == 3:
        api.update_with_media('im.png',("Ha resucitado @"+resucitado+" ... mala hierba nunca muere "))
    return lista

def tweetDuelo(jugador1, jugador2, ganador, perdedor, listaJugadores): # Post the tweet of the fight and his result
    ran = random.randint(1,27)
    if ran == 1:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha dado hasta en el carnet de identidad"))
    elif ran == 2:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha destrozado con un aguacate vietnamita a @"+listaJugadores[perdedor]))
    elif ran == 3:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha estampado la cabeza en el suelo a @"+listaJugadores[perdedor]+" por tirarle el cubata"))
    elif ran == 4:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" se lo ha explicado pero bien a @"+listaJugadores[perdedor]))
    elif ran == 5:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha roto la litrona en la cabeza a @"+listaJugadores[perdedor]))
    elif ran == 6:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" se ha hecho un grinder con los ojos de @"+listaJugadores[perdedor]))
    elif ran == 7:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha colgado de los pies a @"+listaJugadores[perdedor]))
    elif ran == 8:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha metido la sombrilla en el estomago a @"+listaJugadores[perdedor]))
    elif ran == 9:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha reventado los timpanos gritando BEBESITAAAAAHHHHHHH"))
    elif ran == 10:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha cogido a @"+listaJugadores[perdedor])+", le ha metido en el carro del mercadona y le ha tirado por las escaleras")
    elif ran == 11:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha enviado a la casita de campo a @"+listaJugadores[perdedor]))
    elif ran == 12:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha enviado a comer tierra a @"+listaJugadores[perdedor]))
    elif ran == 13:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha hecho un kamehameha"))
    elif ran == 14:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha dado un sopapo fullana @"+listaJugadores[perdedor]))
    elif ran == 15:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha tirado tanto los tejos que ha matado del cansancio a @"+listaJugadores[perdedor]))
    elif ran == 16:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha pinchado la yugular"))
    elif ran == 17:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha pisado el cuello"))
    elif ran == 18:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha encerrado en el horno a @"+listaJugadores[perdedor]))
    elif ran == 19:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha matado degollandolo con una cuerda de pesca"))
    elif ran == 20:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha asesinado atravesandole con un tenedor de plastico"))
    elif ran == 21:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha golpeado con una botella de vodka a @"+listaJugadores[perdedor]))
    elif ran == 22:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha mandado al otro barrio"))
    elif ran == 23:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" ha matado por exceso de belleza @"+listaJugadores[perdedor]))
    elif ran == 24:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha destrozado usando tan solo un dedo"))
    elif ran == 25:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha sacado la pipa a @"+listaJugadores[perdedor]+" y no para mostrarsela..."))
    elif ran == 26:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" ...\n\n@"+listaJugadores[ganador]+" le ha sacado la pipa a @"+listaJugadores[perdedor]+" y no para mostrarsela..."))
    else:
        api.update_with_media('im.png',("SIGUIENTE DUELO DE #GUERRATWITTERXS \n\n@"+jugador1+" se enfrenta contra @"+jugador2+" a beer pong ...\n\n@"+listaJugadores[perdedor]+" no ha sabido aguantar, a la calle"))
# ***************************************** MAIN *****************************************

# INICIALIZACION DE VALORES:

# 1. Cargar jugadores...
listaJugadores = obtenerListaJugadores() #IMPORTAMOS LA LISTA AL INICIO DE JUEGO

# 2. Cargar las bajas...
listaBajas = getListaBajas()    # IMPORTAMOS LA LISTA DE BAJAS
listaBajas = list(map(int,listaBajas))

# 3. Cargar listaEliminados...
listaEliminados = getEliminados()
# 4. Dibujar imagen para inaugurar los juegos del hambre...
dibujarTablero(x,y,listaJugadores)
imagen.save("im.png")

# 5. Subir tweet de inauguracion...
print("QUE EMPIECEN LOS JUEGOS DEL HAMBRE!\n")
api.update_with_media('mjpalomitas.jpg',"QUE EMPIECE LA GUERRA DE TWITTERXS")

# 6. Primer enfrentamiento...
resultado = duelo(listaJugadores, listaEliminados,  listaBajas)
ganador = resultado[0]
perdedor = resultado[1]
listaBajas = actualizarBajas(listaBajas, ganador)
listaEliminados.append(listaJugadores[perdedor])
eliminadosTXT = open('eliminados.txt','w')
for linea in range(len(listaEliminados)):
    eliminadosTXT.write(listaEliminados[linea]+'\n')
eliminadosTXT.close()
# SI SE CORTA EL PROGRAMA PARA SEGUIR EN OTRO MOMENTO, COMENTAR EL PRIMER ENFRENTAMIENTO Y EL TWEET DE INAUGURACION

actualizarTablero(x,y,listaJugadores,listaEliminados)
imagen.save("im.png")
print("El primer enfrentamiento sera entre",resultado[2],"y",resultado[3])
print("Ha ganado @"+listaJugadores[ganador]+"!!!\n\n")
tweetDuelo(resultado[2], resultado[3],ganador, perdedor, listaJugadores)
print('esperando...')
time.sleep(2100)

# Reanudar programa...
#print("QUE CONTINUE LA MASACRE #GUERRATWITTERXS")
#api.update_with_media('mjpalomitas.jpg',"QUE CONTINUE LA MASACRE #GUERRATWITTERXS")
# DESCOMENTAR ESTE APARTADO SI SE REANUDA EL PROGRAMA EN OTRO MOMENTO

# 7. Bucle de duelos....
while len(listaEliminados)<len(listaJugadores)-1:
    #duelo
    resultado = duelo(listaJugadores, listaEliminados,  listaBajas) # realizar un duelo
    # almacenamos ganador y perdedor
    ganador = resultado[0]
    perdedor = resultado[1]
    # actualizamos bajas y eliminados
    listaBajas = actualizarBajas(listaBajas, ganador)
    listaEliminados.append(listaJugadores[perdedor]) # añadir perdedor a eliminados
    eliminadosTXT = open('eliminados.txt','w')
    for linea in range(len(listaEliminados)):
        eliminadosTXT.write(listaEliminados[linea]+'\n')    # reescribir lista
    eliminadosTXT.close()
    # actualizamos tablero
    actualizarTablero(x,y,listaJugadores,listaEliminados)
    imagen.save("im.png")
    print("El siguiente enfrentamiento sera entre",resultado[2],"y",resultado[3])
    print("Ha ganado @"+listaJugadores[ganador]+"!!!\n\n")
    tweetDuelo(resultado[2], resultado[3],ganador, perdedor, listaJugadores)
    print("esperando...")
    time.sleep(2100) # time between the tweets

#tweet ganador/a
print("EL GANADOR/A HA SIDOOO...", listaJugadores[ganador])
api.update_with_media('victoria.jpg',(" Y EL PREMIO MVP ENTRE TODOS LOS TWITTERXS Y GANADOR DEL MEJOR WAR BOT DE LA MARINA, DE LA CV, DE LA FUCKING SPAIN Y DEL PUTO MUNDO EEEESSS....\n\n@"+listaJugadores[ganador]))
