import socket
import pickle
import time
import os

from settings.server import rSrv, ans

if not hasattr(rSrv, 'u') or rSrv.u is None or rSrv.u.getsockname()[1] != rSrv.serverPort:
    print(f'Python UDP server running with port={rSrv.serverPort}')
    rSrv.tStart = time.time()
    rSrv.tcpipinfo = socket.getaddrinfo("localhost", 64588, socket.AF_UNSPEC, socket.SOCK_DGRAM)
    for ii, (family, socktype, proto, canonname, sockaddr) in enumerate(rSrv.tcpipinfo):
        print(f'{ii} - {sockaddr[0]}')

    # Создание сокета сервера
    rSrv.u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rSrv.u.bind((rSrv.serverIp, rSrv.serverPort))
    # Принятие клиентского подключения SamRLSim
    # conn, addr = rSrv.u.accept()
    rSrv.u.connect((rSrv.toIP, rSrv.toPort))
    print("\nПодключение:", (rSrv.toIP, rSrv.toPort))
    # Отправка сообщения удаленному хосту
    rSrv.u.sendto(f'Hello from python mServer {ans}'.encode(), (rSrv.toIP, rSrv.toPort))
    
    while rSrv.cmd != 'exit':
        data = rSrv.u.recvfrom(4096)
        rSrv.cmd = data.decode()
        print(f'Сообщение от клиента: {rSrv.cmd}\n')

        if not rSrv.cmd or rSrv.cmd.startswith('%') or not isinstance(rSrv.cmd, str):
            continue

        rSrv.ki += 1
        try:
            if rSrv.cmd == 'exit':
                break
            elif rSrv.cmd.startswith('edit(') and rSrv.cmd[5:-1].endswith('.py'):
                os.system(f'edit {rSrv.cmd[5:-1]}')
                rSrv.u.sendto(f'Ok. edit={rSrv.cmd[5:-1]}'.encode(), addr)
            else:
                exec(rSrv.cmd, globals())
                if rSrv.cmd.startswith('ans') or 'ans' in globals():
                    ans_str = str(ans)
                    if len(ans_str) > 8000:
                        ans_str = ans_str[:8000] + ' ...'
                    rSrv.u.sendto(f'Ok. ans={ans_str}'.encode(), addr)
                elif rSrv.cmd.startswith('Mi.'):
                    rSrv.u.sendto(f'Ok. Mi.Pi={Mi.Pi} {sum(Mi.Pi)}'.encode(), addr)
                elif rSrv.cmd.startswith('Step'):
                    rSrv.u.sendto(f'Ok. t={t}'.encode(), addr)
                else:
                    rSrv.u.sendto(f'Ok. Time_used={time.time() - rSrv.tStart} s'.encode(), addr)
        except Exception as e:
            if not hasattr(rSrv, 'u'):
                with open('rSrvTemp.pkl', 'rb') as f:
                    rSrv = pickle.load(f)
            rSrv.lastErr = f'{str(e)} In_file: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}'
            print(rSrv.lastErr)
            conn.sendto(rSrv.lastErr.encode(), addr)

    rSrv.u.sendto(f'Bye from mServer. Time_used={time.time() - rSrv.tStart} s'.encode(), addr)
    # print(f'ValuesSent={rSrv.u.sendto.count}; ValuesReceived={rSrv.u.recvfrom.count}; BytesAvailable={rSrv.u.recvfrom.count}')
    rSrv.u.close()
    # print(f'Всего использовано время ЦПУ={time.time() - rSrv.tStart} с')