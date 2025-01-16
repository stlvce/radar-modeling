import socket
import pickle
import time
import os

from settings.server import rSrv, ans

def send_message(msg: str):    
    # Создание сокета для отправки
    rSrv.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rSrv.s.bind((rSrv.serverIp, rSrv.serverSendPort))

    # Подключение к клиентскому SamRLSim
    rSrv.s.connect((rSrv.toIP, rSrv.toPort))

    # Отправка сообщения удаленному хосту
    rSrv.s.sendto(msg.encode(), (rSrv.toIP, rSrv.toPort))
    
    rSrv.s.close()