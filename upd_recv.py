import socket
import pickle
import time
import os

from settings.server import rSrv, ans
from helpers.udp_send import send_message

if not hasattr(rSrv, 'u') or rSrv.u is None or rSrv.u.getsockname()[1] != rSrv.serverRecvPort:
    print(f'Python UDP server running with port={rSrv.serverRecvPort}')
    rSrv.tStart = time.time()
    rSrv.serverinfo = socket.getaddrinfo("localhost", rSrv.serverRecvPort, socket.AF_UNSPEC, socket.SOCK_DGRAM)

    # Создание порта для получение сообщений
    rSrv.u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rSrv.u.bind((rSrv.serverIp, rSrv.serverRecvPort))

    send_message(f'Hello from python mServer {ans}')
    
    while rSrv.cmd != 'exit':
        data = rSrv.u.recvfrom(4096)
        rSrv.cmd = data
        print(f'Сообщение от {data[0]} клиента: {data[1]}\n')

        rSrv.ki += 1
        client_message = rSrv.cmd[0].decode()
        try:
            if 'exit' in client_message:
                break
            elif 'edit(' in client_message and rSrv.cmd[5:-1].endswith('.py'):
                os.system(f'edit {rSrv.cmd[5:-1]}')
                send_message(f'Ok. edit={rSrv.cmd[5:-1]}')
            else:
                exec(rSrv.cmd, globals())
                if 'ans' in client_message or 'ans' in globals():
                    ans_str = str(ans)
                    if len(ans_str) > 8000:
                        ans_str = ans_str[:8000] + ' ...'
                    send_message(f'Ok. ans={ans_str}')
                elif 'Mi.' in client_message:
                    send_message(f'Ok. Mi.Pi={Mi.Pi} {sum(Mi.Pi)}')
                elif 'Step' in client_message:
                    send_message(f'Ok. t={t}')
                else:
                    send_message(f'Ok. Time_used={time.time() - rSrv.tStart} s')
        except Exception as e:
            rSrv.lastErr = f'{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}'
            print(rSrv.lastErr)
            send_message(rSrv.lastErr)
    send_message("UDP server is down")
    # print(f'ValuesSent={rSrv.u.sendto.count}; ValuesReceived={rSrv.u.recvfrom.count}; BytesAvailable={rSrv.u.recvfrom.count}')
    # print(f'Всего использовано время ЦПУ={time.time() - rSrv.tStart} с')