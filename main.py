import socket
import time
import re
from numpy import cos, random

from settings.server import rSrv, ans
from settings.init_variables import *
from helpers import send_message, print_log, get_params
from scripts import (
    process_fm_radar,
    plot_fm_radar_results,
    save_fm_radar_results,
    get_relief,
    get_sea,
    get_traekt,
    calculate_relative_powers,
    show_relief,
    get_mixyz,
)


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

                # Получение из сообщения параметров и команд
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

                # Исполнение команд, print -dmeta можно не исполнять, так как в коде команд создаются изображения
                if "Set_Consts" in commands:
                    send_message("Ok. Consts set")

                if "Get_MiXyZ" in commands:
                    get_mixyz(
                        Nmax=globals()["Mi"].Nmax,
                        Rs=globals()["Mi"].Rs,
                        Rz=globals()["Mi"].Rz,
                        Ry=globals()["Mi"].Ry,
                        Zmax=globals()["Mi"].Zmax,
                        Ymax=globals()["Mi"].Ymax,
                        figext=globals()["test"].figext,
                        result_path="resultFig1.bmp",
                    )

                    send_message("Ok. Get_MiXyZ called")

                if "Get_Traekt" in commands:
                    get_traekt(
                        Nimp=int(globals()["Rs"].Nimp),
                        Xa=int(globals()["Tr"].Xa),
                        Ya=int(globals()["Tr"].Ya),
                        Za=int(globals()["Tr"].Za),
                        Vx=int(globals()["Tr"].Vx),
                        Vy=int(globals()["Tr"].Vy),
                        Vz=int(globals()["Tr"].Vz),
                        St_N=int(globals()["St"].N),
                        St_Xs=int(globals()["Tr"].Xa) + 20,
                        St_Ys=int(globals()["Tr"].Ya),
                        St_Zs=int(globals()["Tr"].Za),
                    )

                    send_message("Ok. Get_Traekt called")

                if "Get_Surface" in commands:
                    send_message("Ok. Get_Surface called")

                if "Do_Step" in commands:
                    send_message("Ok. Do_Step called")

                if "Do_SignMod" in commands:
                    send_message("Ok. Do_SignMod called")

                if "Get_Relief" in commands:
                    Sf, Relief = get_relief(globals())
                    show_relief(Relief)

                    send_message("Ok. Get_Relief called")

                if "Do_SintFM" in commands:
                    test_globals = {
                        "dtau": 1e-6,
                        "c": 3e8,
                        "Wd": 1e6,
                        "H": 1.0,
                        "ChannelN": 3,
                        "Nimp": 64,
                        "Timp": 1e-2,
                        "SigCN": random.rand(3, 100, 100),
                        "SigSN": random.rand(3, 100, 100),
                        "Rs": {"Rmin": 0.0, "Rmax": 1000, "Log": True, "GB": 20},
                    }
                    test_globals = process_fm_radar(test_globals)
                    plot_fm_radar_results(test_globals)
                    save_fm_radar_results(test_globals)
                    send_message("Ok. Do_SintFM called")

            # Ждём следующей итерации
            except socket.timeout:
                continue

            # Обработка ошибок
            except Exception as e:
                if e.__traceback__ is not None:
                    rSrv.lastErr = f"{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}"
                else:
                    rSrv.lastErr = f"{str(e)}"
                print(f"\n{rSrv.lastErr}")
                send_message(rSrv.lastErr)

    # Обработка остановки сервера при Ctrl+C
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped manually via Ctrl+C")

    # Отключение сервера при KeyboardInterrupt и команды "exit"
    finally:
        send_message("Ok. UDP server is down")
        rSrv.u.close()


# Запуск сервера
if __name__ == "__main__":
    server_run()
