import tweepy
import time
import sys

print("Hello world")

CONSUMER_KEY # clave privada srry
CONSUMER_SECRET # clave privada srry
ACCESS_KEY # clave privada srry
ACCESS_SECRET # clave privada srry

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FICHERO = "last_seen_id.txt"

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r+')
    last_seen_id = int(f_read.read().strip("\n"))
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
def responder():
    print("respondiendo...")
    last_seen_id = retrieve_last_seen_id(FICHERO)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')

    for mention in reversed(mentions):
        print(str(mention.id)+' - '+mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FICHERO)
        if '#guerratwitterxs' in mention.full_text.lower():
            print("found #guerratwitterxs!")
            print("Twitteado por ",mention.user.name)
            api.create_favorite(mention.id)
            anadirJugador(mention.user.screen_name)

def anadirJugador(nombre):
    contador = 33
    listaJugadores = open('listaJugadores.txt','a')
    nombre += "\n"
    listaJugadores.write(nombre)
    contador +=1
    listaJugadores.close()
    if contador == 154:
        sys.exit()

while True:
    responder()
    time.sleep(15)