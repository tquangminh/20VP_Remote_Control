import socket

# HOST = input("Enter IP: ")
#----
PORT = 1239
HOST = '192.168.160.132'
try:
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, PORT))
    cli.sendall('Client'.encode("utf8"))
    cli.recv(1024)
    print("Connect to Server successfully")
except:
    print("Connection Lost", "Server has disconnected")

# # get process List
# req = input("Request: ")
# cli.sendall(req.encode("utf8"))
# res = cli.recv(50000).decode("utf8")
# print(res)
# #kill Process
# req = 'kill'
# cli.sendall(req.encode("utf8"))
# res = cli.recv(50000).decode("utf8")
# req = input("Request: ")
# cli.sendall(req.encode("utf8"))
# res = cli.recv(1024).decode("utf8")

# capture
# req = 'printScreen'
# cli.sendall(req.encode("utf8"))
# image = cli.recv(500000)   
# # writing it to the disk using opencv
# with open('screenshot.jpg', "wb") as f:
#     f.write(image) 

#keystroke
# req = 'keystroke'
# cli.sendall(req.encode("utf8"))
# cli.recv(1024)
# #hook
# req = input('request: ')
# cli.sendall(req.encode("utf8"))
# cli.recv(1024)
# #unhook
# req = input('request: ')
# cli.sendall(req.encode("utf8"))
# cli.recv(1024)
# #view
# req = input('request: ')
# cli.sendall(req.encode("utf8"))
# string = cli.recv(1024).decode('utf8')
# print(string)

# shutdown
req = input('Request')
cli.sendall(req.encode("utf8"))
cli.recv(1024)






