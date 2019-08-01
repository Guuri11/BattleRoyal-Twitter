import tweepy
from PIL import Image, ImageFont, ImageDraw

CONSUMER_KEY # clave privada srry
CONSUMER_SECRET # clave privada srry
ACCESS_KEY # clave privada srry
ACCESS_SECRET # clave privada srry

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def obtenerListraJugadores():
    listaJugadores = open('listaJugadores.txt', 'r')
    lista = []
    for linea in listaJugadores:
        linea = linea.rstrip("\n")
        lista.append(linea)
    return lista
    listaJugadores.close()

def dibujarTablero(x,y,lista):
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
        
imagen = Image.new('RGBA',(1400,1200),'white')
font = ImageFont.truetype('arial.ttf',30,0,'utf-8',None)

draw = ImageDraw.Draw(imagen)
x = 50
y = 50
fila = 10
columna = 10
listaJugadores = obtenerListraJugadores()
dibujarTablero(x,y,listaJugadores)

imagen.save("im.png")
tweet = "Bueno gente... Ahora si que si, se acabo el plazo de inscripcion!! Estxs son lxs 100 participantes jeje"
api.update_with_media('im.png',tweet)