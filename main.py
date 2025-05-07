import socket
import time
import re

from settings.server import rSrv, ans
from settings.init_variables import *  # noqa: F403
from helpers import send_message, print_log, set_consts
from parsers import parse_colon
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
                # Обработка выхода
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

                # Отправка времени работы сервера
                elif "server time" in rSrv.cmd:
                    send_message(
                        f"Ok. Server uptime - {round(time.time() - rSrv.tStart)} s"
                    )

                # elif "Set_Consts;" in rSrv.cmd:
                #     set_consts(rSrv.cmd)
                #     send_message("Ok. Consts set")

                # Установка констант
                elif (
                    "Set_Consts;" in rSrv.cmd
                    or "Get_Traekt; print -dmeta" in rSrv.cmd
                    or "Get_Surface; print -dmeta" in rSrv.cmd
                ):
                    for el in vars:
                        # Если переменной нет, то продожаем цикл
                        if el == "":
                            continue

                        curr_var = el

                        # Убираем скобки из переменной
                        if "(" in el and ")=" in el:
                            curr_var = "".join("".join(el.split("(")).split(")"))

                        if "{" in el and "}=" in el:
                            curr_var = "".join("".join(el.split("{")).split("}"))

                        # Убираем двоеточие из переменной
                        if ":" in el:
                            curr_var = parse_colon(el)

                        # Убираем двоеточие из переменной
                        if ":" in el or ("evs" in el and "'" not in el):
                            curr_var = "='".join(el.split("=")) + "'"

                        # Выполняем присваивание
                        print("Текущая переменая", curr_var)
                        exec(curr_var, globals())

                    send_message("Ok. Vars created")

                # Выполнение строк кода
                elif "print(z)" in rSrv.cmd:
                    test_str = "\n".join(rSrv.cmd.split(" "))
                    print(test_str)
                    x = compile(test_str, "test", "exec")
                    exec(x)

                # Операция присвивания
                elif "set" in rSrv.cmd and "=" in rSrv.cmd:
                    pattern = r"set\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^;]+)"
                    match = re.search(pattern, rSrv.cmd)
                    if match:
                        assignment = match.group(1)
                        exec(assignment, globals())

                # Выполнение строки кода
                else:
                    result = eval(rSrv.cmd, globals())
                    send_message(f"Ok. {str(result)}")

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
