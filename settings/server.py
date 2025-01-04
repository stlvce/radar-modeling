from socket import socket

ans = 'v.2.2'

class rSrv:
    serverIp = ""
    serverPort = 9099
    serverPortRecv = 9098
    toPort = 9092
    toIP = "localhost"
    tcpipinfo = None
    u_list = []
    u: socket | None = None
    tStart = 0
    cmd = ''
    ki = 0
    lastErr = ''