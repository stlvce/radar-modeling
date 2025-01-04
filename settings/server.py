from socket import socket

ans = 'v.2.2'

class rSrv:
    serverIp = ""
    serverPort = 9099
    serverRecvPort = 9098
    toPort = 9092
    toIP = "localhost"
    serverinfo = None
    u: socket | None = None
    s: socket | None = None
    tStart = 0
    cmd = ''
    ki = 0
    lastErr = ''