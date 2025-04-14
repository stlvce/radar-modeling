import socket
import pickle
import time
from datetime import datetime
import os
import numpy as np
import re

from settings.server import rSrv, ans
from helpers.send_message import send_message
from helpers.run_cmd import run_cmd
from test.test_func import test_func

class Rs:
    pass

class Mi:
    pass

class test:
    pass

class St:
    pass

class Tr:
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
    rSrv.u.settimeout(1.0)  # Устанавливаем таймаут в 1 секунду
    # Отправка приветственного сообщения 
    send_message(f'Hello from python mServer {ans}')

    try:
        while rSrv.cmd != 'exit':
            try:
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
                # Обработка выхода
                if "exit" in rSrv.cmd:
                    break
                # Вывод ans версии
                if "ans" in rSrv.cmd:
                    ans_str = str(ans)
                    if len(ans_str) > 8000:
                        ans_str = ans_str[:8000] + " ..."
                    send_message(f"Ok. ans={ans_str}")
                # Отправка времени работы сервера
                elif "server time" in rSrv.cmd:
                    send_message(f"Ok. Server uptime - {time.time() - rSrv.tStart} s")
                # Запуска файлов с расширением .py
                elif ".py" in rSrv.cmd:
                    cmd_result = run_cmd(rSrv.cmd)
                    send_message(f"Ok. Result of the command: {cmd_result}")
                # Установка констант
                elif "Set_Consts;" in rSrv.cmd or "Get_Traekt; print -dmeta" in rSrv.cmd:
                    # Создание массива переменных
                    arr = rSrv.cmd[12:len(rSrv.cmd)-25].split("; ")
                    for el in arr:
                        print("Текущая переменая", el)
                        # Если переменной нет, то продожаем цикл
                        if el == "":
                            continue
                        
                        # Убираем скобки из переменной
                        if "(" in el and ")=" in el:
                            exec("".join("".join(el.split("(")).split(")")), globals())
                            continue
                        
                        # Убираем двоеточие из переменной
                        if ":" in el or ("evs" in el and "'" not in el):
                            exec("='".join(el.split("="))+"'", globals())
                            continue
                        
                        # Выполняем присваивание
                        exec(el, globals())
                # Выполнение строк кода
                elif "print(z)" in rSrv.cmd:
                    test_str = "\n".join(rSrv.cmd.split(" "))
                    print(test_str)
                    x = compile(test_str, 'test', 'exec')
                    exec(x)
                # Операция присвивания
                elif "set" in rSrv.cmd and "=" in rSrv.cmd:
                    pattern = r'set\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^;]+)'
                    match = re.search(pattern, rSrv.cmd)
                    if match:
                        assignment = match.group(1)
                        exec(assignment, globals())
                # Выполнение строки кода
                else:
                    result = eval(rSrv.cmd, globals())
                    send_message(str(result))
            
            except socket.timeout:
                continue  # просто ждём следующей итерации
            # Обработка ошибок
            except Exception as e:
                rSrv.lastErr = f'{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}'
                print(f"\n{rSrv.lastErr}")
                send_message(rSrv.lastErr)

    except KeyboardInterrupt:
        print("\n[INFO] Server stopped manually via Ctrl+C")

    finally:
        # Сообщение об остановке работы сервера
        send_message("Ok. UDP server is down")
        rSrv.u.close()   

server_run()