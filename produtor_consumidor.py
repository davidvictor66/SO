from threading import Thread, Lock
import time
import random
from threading import Condition

buffer = []
lock = Lock()
MAX_NUM = 5

condition = Condition()

class ConsumidorThread(Thread):
    def run(self):
        global buffer
        while True:
            condition.acquire() #entrar na região crítica
            if not buffer: #se não tiver nada no buffer
                print ("Nada no Buffer, consumidor em espera")
                condition.wait() #espera até que notify() seja chamado
                print ("Produtor adicionou algo ao buffer, e liberou o consumidor")
            num = buffer.pop(0) #tira o valor da posição 0
            print ("Consumido", num)
            condition.notify()
            condition.release() #sair da região crítica
            time.sleep(5)


class ProdutorThread(Thread):
    def run(self):
        nums = range(MAX_NUM)
        global buffer
        while True:
            condition.acquire()
            if len(buffer) == MAX_NUM:
                print ("Buffer cheio, produtor esperando")
                condition.wait()
                print ("Espaço liberdo, produtor iniciado")
            num = random.choice(nums) #pega um valor aleatorio 
            buffer.append(num) #adiciona ao buffer
            print ("Produzido", num)
            print (len(buffer))
            condition.notify()
            condition.release()
            time.sleep(2)


ProdutorThread().start()
ConsumidorThread().start()
