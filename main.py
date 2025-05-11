import socket
import time
import re

from settings.server import rSrv, ans
from settings.init_variables import *  # noqa: F403
from helpers import send_message, print_log, get_params
from test.test_func import *  # noqa: F403


def server_run():
    print(f"UDP server running with port {rSrv.serverRecvPort}")
    rSrv.tStart = time.time()  # Время запуска программы
    rSrv.serverinfo = socket.getaddrinfo(
        "localhost", rSrv.serverRecvPort, socket.AF_UNSPEC, socket.SOCK_DGRAM
    )  # Информация о сервере
    rSrv.u = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM
    )  # Создание порта для получение сообщений
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

                parsed_params = get_params(vars)

                # Установка констант
                if "Set_Consts" in commands:
                    # Выполняем присваивание
                    for el in parsed_params:
                        print("Текущая константа", el)
                        exec(el, globals())

                    send_message("Ok. Consts setted")

                if "Get_MiXyZ" in commands:
                    send_message("Ok. Get_MiXyZ called")

                if "Get_Traekt" in commands:
                    # Выполняем присваивание
                    for el in parsed_params:
                        print("Параметр", el)
                        exec(el, globals())

                    send_message("Ok. Get_Traekt called")

                if "Get_Surface" in commands:
                    # Выполняем присваивание
                    for el in parsed_params:
                        print("Параметр", el)
                        exec(el, globals())

                    send_message("Ok. Get_Surface called")

                if "Do_Step" in commands:
                    # Выполняем присваивание
                    for el in parsed_params:
                        print("Параметр", el)
                        exec(el, globals())

                    send_message("Ok. Do_Step called")

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

                # Выполнение строки кода
                # result = eval(rSrv.cmd, globals())
                # send_message(f"Ok. {str(result)}")

            except socket.timeout:
                continue  # ждём следующей итерации

            # Обработка ошибок
            except Exception as e:
                rSrv.lastErr = f"{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}"
                print(f"\n{rSrv.lastErr}")
                send_message(rSrv.lastErr)

    except KeyboardInterrupt:
        print("\n[INFO] Server stopped manually via Ctrl+C")

    finally:
        # Отключение сервера при KeyboardInterrupt и команды "exit"
        send_message("Ok. UDP server is down")
        rSrv.u.close()


if __name__ == "__main__":
    server_run()
