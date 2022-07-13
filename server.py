import socket
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox 
import json
import threading
import sqlite3
import sys
import os

def threaded_client(con, addr):
    while True: 
        req = con.recv(1024).decode("utf8")
        if req == "processList": 
            output = os.popen('wmic process get description, processid').read()
            print("Size" + str(sys.getsizeof(output)))
            print("Len" + str(len(output)))
            con.sendall(output.encode("utf8)"))
        if req == "kill":
            con.sendall("Receive Request".encode('utf8'))
            pId = con.recv(1024).decode('utf8')
            os.popen('taskkill /F /PID ' + pId)
            con.sendall("Kill process".encode('utf8'))
        

    con.close()

#def start server:
def start_server():
    print("Start")
    while True:
        try:
            con, addr = s.accept()
            print("Connected to: " + str(addr))
            iden = con.recv(1024).decode("utf8")
            if iden == "Client":
                con.sendall("Welcome Client".encode("utf8"))
                client = threading.Thread(target=threaded_client, args=(con,addr))
                client.daemon = True
                client.start()
        except:
            print("Disconnect")
            break
            


#server_thread
def server_thread():
    root.config(bg="#2ecc71")
    global stop_thread
    stop_thread = False

    global check
    if check == 1:
        messagebox.showinfo("Status", "Server has been running")
        return

    check = 1

    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    HOST = str(ip_addr)
    PORT = 1239

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    s.listen(5)
    print("IP: " + HOST + '; Port: ' + str(PORT))
    print("Waiting for a Connection...")

    sv = threading.Thread(target=start_server)
    sv.daemon = True
    sv.start()

def add_and_close():
	root.config(bg="white")
	global check
	global stop_thread
	if check == 0:
		messagebox.showinfo("Status", "Server has not been started yet")
		return
	
	check = 0

	stop_thread = True
	s.close()
	print("Close Server")


#MAIN
check = 0


#Server Window
root = Tk()
root.title("Server")

style = ttk.Style()
style.configure('TButton', font =
			('calibri', 20, 'bold'))

style.map('W.TButton', foreground = [('active', 'black')],
					background = [('active', '#DC143C')])

style.map('TButton', foreground = [('active','!disabled', 'black')],
					background = [('active', '#9ACD32')])

btn1 = Button(root, text = 'Start Server', command = server_thread)
btn1.grid(ipadx = 30, ipady=30,padx=20,pady=10)

btn2 = Button(root, text = 'Disconnect',style="W.TButton", command = add_and_close)
btn2.grid(ipadx = 30, ipady=30,padx=20,pady=10)

root.mainloop()