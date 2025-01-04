import socket
import pickle
import time
import os

from settings.server import rSrv, ans
from helpers.udp_send import send_message

if not hasattr(rSrv, 'u') or rSrv.u is None or rSrv.u.getsockname()[1] != rSrv.serverRecvPort:
    print(f'Python UDP server running with port={rSrv.serverRecvPort}')
    rSrv.tStart = time.time()
    rSrv.serverinfo = socket.getaddrinfo("localhost", 64588, socket.AF_UNSPEC, socket.SOCK_DGRAM)

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
        print(client_message)
        try:
            if 'exit' in client_message:
                break
            elif 'edit(' in client_message and rSrv.cmd[5:-1].endswith('.py'):
                os.system(f'edit {rSrv.cmd[5:-1]}')
                # rSrv.u.sendto(f'Ok. edit={rSrv.cmd[5:-1]}'.encode(), addr)
            else:
                exec(rSrv.cmd, globals())
                if 'ans' in client_message or 'ans' in globals():
                    ans_str = str(ans)
                    if len(ans_str) > 8000:
                        ans_str = ans_str[:8000] + ' ...'
                    # rSrv.u.sendto(f'Ok. ans={ans_str}'.encode(), addr)
                elif 'Mi.' in client_message:
                    print(client_message)
                    # rSrv.u.sendto(f'Ok. Mi.Pi={Mi.Pi} {sum(Mi.Pi)}'.encode(), addr)
                elif 'Step' in client_message:
                    print(client_message)
                    # rSrv.u.sendto(f'Ok. t={t}'.encode(), addr)
                else:
                    print(client_message)
                    # rSrv.u.sendto(f'Ok. Time_used={time.time() - rSrv.tStart} s'.encode(), addr)
        except Exception as e:
            rSrv.lastErr = f'{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}'
            print(rSrv.lastErr)
            # conn.sendto(rSrv.lastErr.encode(), addr)

    # print(f'ValuesSent={rSrv.u.sendto.count}; ValuesReceived={rSrv.u.recvfrom.count}; BytesAvailable={rSrv.u.recvfrom.count}')
    # print(f'Всего использовано время ЦПУ={time.time() - rSrv.tStart} с')