import socket
import pickle
import time
from datetime import datetime
import os

from settings.server import rSrv, ans
from helpers.send_message import send_message
from helpers.run_cmd import run_cmd

class Rs:
    pass

class Mi:
    pass

class test:
    pass

def server_run():
    print(f'UDP server running with port {rSrv.serverRecvPort}')
    # Время запуска программы
    rSrv.tStart = time.time()
    # Информация о сервере
    rSrv.serverinfo = socket.getaddrinfo("localhost", rSrv.serverRecvPort, socket.AF_UNSPEC, socket.SOCK_DGRAM)
    # Создание порта для получение сообщений
    rSrv.u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rSrv.u.bind((rSrv.serverIp, rSrv.serverRecvPort))
    # Отправка приветственного сообщения 
    send_message(f'Hello from python mServer {ans}')
    while rSrv.cmd != 'exit':
        # Получение сообщения
        data = rSrv.u.recvfrom(4096)
        rSrv.cmd = data[0].decode()

        # Вывод в логи
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{formatted_datetime}")
        print(f"Сообщение: {rSrv.cmd}")
        print(f"Отправитель: {data[1]}")

        # Выполнение команды из сообщения
        try:
            if "exit" in rSrv.cmd:
                break
            if "ans" in rSrv.cmd:
                ans_str = str(ans)
                if len(ans_str) > 8000:
                    ans_str = ans_str[:8000] + " ..."
                send_message(f"Ok. ans={ans_str}")
            elif "server time" in rSrv.cmd:
                send_message(f"Ok. Server uptime - {time.time() - rSrv.tStart} s")
            elif ".py" in rSrv.cmd:
                cmd_result = run_cmd(rSrv.cmd)
                send_message(f"Ok. Result of the command: {cmd_result}")
            elif "Set_Consts;" in rSrv.cmd:
                arr = rSrv.cmd[12:len(rSrv.cmd)-25].split("; ")
                for el in arr:
                    print("Текущая переменая", el)
                    if el == "":
                        continue

                    if "(" in el:
                        exec("".join("".join(el.split("(")).split(")")), globals())
                        continue

                    if ":" in el:
                        exec("='".join(el.split("="))+"'", globals())
                        continue
                    exec(el, globals())
            elif "=" in rSrv.cmd:
                print(type(rSrv.cmd))
                exec(rSrv.cmd, globals())
            else:
                result = eval(rSrv.cmd, globals())
                send_message(str(result))
                
        except Exception as e:
            rSrv.lastErr = f'{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}'
            print(f"\n{rSrv.lastErr}")
            send_message(rSrv.lastErr)
    
    # Сообщение об остановке работы сервера
    send_message("Ok. UDP server is down")

server_run()
    