import socket

from settings.server import rSrv

sock = socket.socket()
print("CLIENT START")
sock.bind((rSrv.toIP, rSrv.toPort))
sock.connect((rSrv.serverIp, rSrv.serverPort))
sock.sendto('hello, world!'.encode(), (rSrv.serverIp, rSrv.serverPort))


while True:
  s = input()
  if s == "exit":
    data = sock.recv(1024)
    print(data)
    break
  data = sock.recv(1024)
  print(data)

sock.sendto('exit'.encode(), (rSrv.serverIp, rSrv.serverPort))

