import socket
import sys

HOST = input("Enter IP: ")
#----
PORT = 1239

try:
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, PORT))
    cli.sendall('Client'.encode("utf8"))
    cli.recv(1024)
    print("Connect to Server successfully")
except:
    print("Connection Lost", "Server has disconnected")

#get process List
req = input("Request: ")
req = 'processList'
cli.sendall(req.encode("utf8"))
res = cli.recv(50000).decode("utf8")
print("Size" + str(len(res)))
print(res)
#kill Process
req = 'kill'
cli.sendall(req.encode("utf8"))
res = cli.recv(50000).decode("utf8")
req = input("Request: ")
cli.sendall(req.encode("utf8"))
res = cli.recv(1024).decode("utf8")


