import threading
from threading import Thread
import time
import random

MAX_BARBEIROS=3
MAX_CADEIRAS=5
LIVRE=0
OCUPADO=1
estado_barbeiro=[]
semaforo_barbeiro=[]
semaforo_barbeiro_durmir=[]
lista_espera=[]
estado_semaforo=[]
semaforo_cliente0=threading.Semaphore(1)

for i in range(MAX_BARBEIROS):
    semaforo_barbeiro.append(threading.Semaphore(1))
    semaforo_barbeiro_durmir.append(threading.Semaphore(1))
    estado_barbeiro.append(LIVRE)
    estado_semaforo.append(1)

def Barbeiro(n):
    global lista_espera
    while True:
        if len(lista_espera)==0:
            estado_semaforo[n]-=1
            semaforo_barbeiro_durmir[n].acquire() #bloquea o barbeiro para durmir e esperar
            if estado_barbeiro[n]==LIVRE:
                print("Barbeiro",n+1,"dormindo")
            else:
                print("Barbeiro",n+1,"acordou")
        else:
            semaforo_barbeiro[n].acquire() #bloqueia o barbeiro
            semaforo_cliente0.acquire() #bloqueia o proximo cliente, para que dois barbeiros não peguem o mesmo
            print("Barbeiro",n+1,"cortando cabelo do cliente",lista_espera[0])
            del lista_espera[0]
            semaforo_cliente0.release()
            time.sleep(random.randint(4, 6)) #tempo para cortar o cabelo
            estado_barbeiro[n] = LIVRE
            print("Barbeiro",n+1,"livre")
            semaforo_barbeiro[n].release()
            if estado_semaforo[n]==0:
                estado_semaforo[n] += 1
                semaforo_barbeiro_durmir[n].release()

class Cliente(Thread):
    def run(self):
        global lista_espera
        cliente = 1
        while True:
            time.sleep(random.randint(1, 2)) #tempo para chegar proximo cliente
            print("Cliente numero",cliente,"entrou")
            if len(lista_espera)<MAX_CADEIRAS:
                lista_espera.append(cliente)
                print("Lista de espera:",lista_espera)
                for i in range(MAX_BARBEIROS):
                    if estado_barbeiro[i]==LIVRE:
                        estado_barbeiro[i]=OCUPADO
                        if estado_semaforo[i]<0: #impede que faça muitos release em semaforo_barbeiro_durmir
                            estado_semaforo[i] += 1
                            semaforo_barbeiro_durmir[i].release()
                        break #sai do laço para que mais de um barbeiro seja chamado para o mesmo cliente
            else:
                print("Barbearia cheia cliente numero",cliente,"saiu")
            cliente+=1

threads = []
for i in range(MAX_BARBEIROS):
   threads.append(Thread(target=Barbeiro, args=[i]))
   threads[i].start()
Cliente().start()