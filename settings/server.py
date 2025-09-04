from socket import socket

ans = "v.2.2"


class rSrv:
    serverIp = ""
    serverSendPort = 9099
    serverRecvPort = 9098
    toIP = "localhost"
    toPort = 9092
    serverinfo: list[tuple] | None = None
    u: socket | None = None
    s: socket | None = None
    tStart = 0
    cmd = ""
    lastErr = ""
    tStart: float
