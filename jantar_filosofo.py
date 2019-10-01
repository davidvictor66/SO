import threading
from threading import Thread
import time
import random

MAX_FILOSOFOS= 2
semaforo_filosofos=[]
semaforo_garfos=[]
semaforo_pegar_garfos=threading.Semaphore(1)
estado_filosofos=[]
estado_semaforo=[]
PENSANDO = 0
COMENDO = 1
DORMINDO= 2

for i in range(MAX_FILOSOFOS):
    estado_filosofos.append(PENSANDO)
    semaforo_filosofos.append(threading.Semaphore(1))
    semaforo_garfos.append(threading.Semaphore(1))
    estado_semaforo.append(1)

def filosofo(n_filosofo):
    while True:
        print("Filosofo",n_filosofo+1,"com fome")
        print("Filosofo", n_filosofo+1, "tentando pegar os garfos")
        pega_garfo(n_filosofo)
        time.sleep(random.randint(2, 3)) #tempo para sentir fome de novo

def pega_garfo(n_filosofo):
    filosofo_direita = (n_filosofo + 1) % MAX_FILOSOFOS
    filosofo_esquerda= (n_filosofo + MAX_FILOSOFOS-1) % MAX_FILOSOFOS
    if (estado_filosofos[filosofo_direita] == PENSANDO or estado_filosofos[filosofo_direita] == DORMINDO) and \
            (estado_filosofos[filosofo_esquerda] == PENSANDO or estado_filosofos[filosofo_esquerda] == DORMINDO):
        semaforo_pegar_garfos.acquire()
        semaforo_garfos[n_filosofo].acquire()
        time.sleep(2)
        semaforo_garfos[filosofo_direita].acquire()
        semaforo_pegar_garfos.release()
        estado_filosofos[n_filosofo] = COMENDO
        print("Filosofo", n_filosofo+1, "comendo")
        time.sleep(random.randint(2, 3)) #tempo para comer
        larga_garfo(n_filosofo)
    else:
        if estado_semaforo[n_filosofo]==1:
            print("Garfos para o filosofo", n_filosofo+1, "ocupado")
            print("Filosofo",n_filosofo+1,"dormindo")
            estado_filosofos[n_filosofo] = DORMINDO
        estado_semaforo[n_filosofo]-=1
        if estado_semaforo[n_filosofo]==-1:
            estado_filosofos[n_filosofo]=DORMINDO
        semaforo_filosofos[n_filosofo].acquire()
        if (estado_filosofos[filosofo_direita] == PENSANDO or estado_filosofos[filosofo_direita] == DORMINDO) and \
                (estado_filosofos[filosofo_esquerda] == PENSANDO or estado_filosofos[filosofo_esquerda] == DORMINDO):
            print("Filosofo", n_filosofo + 1, "acordou")
            semaforo_filosofos[n_filosofo].release()
            estado_semaforo[n_filosofo] += 1
        pega_garfo(n_filosofo)


def larga_garfo(n_filosofo):
    print("Filosofo", n_filosofo + 1, "largou os garfos")
    print("Filosofo", n_filosofo + 1, "pensando")
    filosofo_direita = (n_filosofo + 1) % MAX_FILOSOFOS
    filosofo_esquerda= (n_filosofo + MAX_FILOSOFOS-1) % MAX_FILOSOFOS
    if estado_filosofos[filosofo_esquerda] == DORMINDO:
        estado_filosofos[filosofo_esquerda] = PENSANDO
        estado_semaforo[filosofo_esquerda] += 1
        semaforo_filosofos[filosofo_esquerda].release()
    if estado_filosofos[filosofo_direita] == DORMINDO:
        estado_filosofos[filosofo_direita]=PENSANDO
        estado_semaforo[filosofo_direita]+=1
        semaforo_filosofos[filosofo_direita].release()
    semaforo_garfos[n_filosofo].release()
    semaforo_garfos[filosofo_direita].release()
    estado_filosofos[n_filosofo]=PENSANDO

threads = []
for i in range(MAX_FILOSOFOS):
   threads.append(Thread(target=filosofo, args=[i]))
   threads[i].start()
   time.sleep(random.randint(3, 6))