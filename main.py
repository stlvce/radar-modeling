import socket
import time
import re

from settings.server import rSrv, ans
from settings.init_variables import *  # noqa: F403
from helpers import send_message, print_log, get_params
from scripts import get_relief, show_relief


def server_run():
    print(f"UDP server running with port {rSrv.serverRecvPort}")
    rSrv.tStart = time.time()  # Время запуска программы
    rSrv.serverinfo = socket.getaddrinfo(
        "localhost", rSrv.serverRecvPort, socket.AF_UNSPEC, socket.SOCK_DGRAM
    )  # Информация о сервере
    rSrv.u = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM
    )  # Создание порта для получения сообщений
    rSrv.u.bind((rSrv.serverIp, rSrv.serverRecvPort))
    rSrv.u.settimeout(1.0)  # Устанавливаем таймаут в 1 секунду
    send_message(
        f"Hello from python mServer {ans}"
    )  # Отправка приветственного сообщения

    try:
        while rSrv.cmd != "exit":
            try:
                # Получение сообщения
                data = rSrv.u.recvfrom(4096)
                rSrv.cmd = data[0].decode()
                print_log(rSrv.cmd, data[1])

                # Выполнение команды из сообщения
                if "exit" in rSrv.cmd:
                    break

                vars = []
                commands = []

                for i in rSrv.cmd.split("; "):
                    if i.strip() == "":
                        continue

                    if "=" in i:
                        vars.append(i)
                    else:
                        commands.append(i)

                # Вывод ans версии
                if "ans" in rSrv.cmd:
                    ans_str = str(ans)
                    if len(ans_str) > 8000:
                        ans_str = ans_str[:8000] + " ..."
                    send_message(f"Ok. ans={ans_str}")
                    continue

                # Отправка времени работы сервера
                if "server time" in rSrv.cmd:
                    send_message(
                        f"Ok. Server uptime - {round(time.time() - rSrv.tStart)} s"
                    )
                    continue

                # Выполняем присваивание
                parsed_params = get_params(vars)
                for el in parsed_params:
                    print("Параметр", el)
                    exec(el, globals())

                # Исполнение команд
                if "Set_Consts" in commands:
                    send_message("Ok. Consts set")

                if "Get_MiXyZ" in commands:
                    send_message("Ok. Get_MiXyZ called")

                if "Get_Traekt" in commands:
                    send_message("Ok. Get_Traekt called")

                if "Get_Surface" in commands:
                    send_message("Ok. Get_Surface called")

                if "Do_Step" in commands:
                    send_message("Ok. Do_Step called")

                if "Do_SignMod" in commands:
                    send_message("Ok. Do_SignMod called")

                if "Get_Relief" in commands:
                    Sf, Relief = get_relief(globals())
                    relief_img = show_relief(Relief)
                    print(f"Sf={Sf.__dict__} Relief={Relief}")

                    send_message("Ok. Get_Relief called")
                    send_message(relief_img)

                if "print -dmeta" in commands:
                    send_message("Ok. print -dmeta called")

                # Операция присвивания | Пример: set a=1
                if "set" in rSrv.cmd and "=" in rSrv.cmd:
                    pattern = r"set\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^;]+)"
                    match = re.search(pattern, rSrv.cmd)
                    if match:
                        assignment = match.group(1)
                        exec(assignment, globals())
                    continue

            except socket.timeout:
                continue  # ждём следующей итерации

            # Обработка ошибок
            except Exception as e:
                if e.__traceback__ is not None:
                    rSrv.lastErr = f"{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}"
                else:
                    rSrv.lastErr = f"{str(e)}"
                print(f"\n{rSrv.lastErr}")
                send_message(rSrv.lastErr)

    except KeyboardInterrupt:
        print("\n[INFO] Server stopped manually via Ctrl+C")

    finally:
        send_message("Ok. UDP server is down")
        rSrv.u.close()  # Отключение сервера при KeyboardInterrupt и команды "exit"


# Запуск сервера
if __name__ == "__main__":
    server_run()
