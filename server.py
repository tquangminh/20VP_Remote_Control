import socket, threading
from tkinter import Tk, ttk, messagebox 
from tkinter.ttk import *
import sys, os, io
import pyautogui, keyboard

def threaded_client(con, addr):
    while True: 
        req = con.recv(1024).decode("utf8")
        if req == 'process':
            con.sendall("Receveid request".encode('utf8'))

            while True:
                req = con.recv(1024).decode("utf8")
                if req == "processList": 
                    output = os.popen('powershell \"gps | select ProcessName, Id, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}} | ConvertTo-Csv').read()
                    con.sendall(output.encode("utf8)"))
                elif req == "kill":
                    con.sendall("Receive Request".encode('utf8'))
                    pId = con.recv(1024).decode('utf8')
                    os.popen('taskkill /F /PID ' + pId)
                    con.sendall("Kill process".encode('utf8'))
                elif req == "start":
                    con.sendall("Receive Request".encode('utf8'))
                    name = con.recv(1024).decode('utf8')
                    os.popen('start ' + name)
                    con.sendall("start process".encode('utf8'))
                if req == 'process closing':
                    con.sendall('Received request'.encode('utf8'))
                    break
        if req == 'app':
            con.sendall("Receveid request".encode('utf8'))

            while True:
                req = con.recv(1024).decode("utf8")
                if req == "appList": 
                    output = os.popen('powershell \"gps | where {$_.MainWindowTitle } | select ProcessName, Id, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}} | ConvertTo-Csv').read()
                    con.sendall(output.encode("utf8)"))
                elif req == "kill":
                    con.sendall("Receive Request".encode('utf8'))
                    pId = con.recv(1024).decode('utf8')
                    os.popen('taskkill /F /PID ' + pId)
                    con.sendall("Kill app".encode('utf8'))
                elif req == "start":
                    con.sendall("Receive Request".encode('utf8'))
                    name = con.recv(1024).decode('utf8')
                    os.popen('start ' + name)
                    con.sendall("start app".encode('utf8'))
                if req == 'app closing':
                    con.sendall('Received request'.encode('utf8'))
                    break

        if req == "printScreen":
            img = pyautogui.screenshot()
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            con.sendall(img_byte_arr)

        if req == "keystroke":
            con.sendall("receveived Request".encode("utf8"))
            req = con.recv(1024).decode("utf8")
            if req == "hook":
                keyboard.start_recording() 
                con.sendall("Hooked".encode("utf8"))
            req = con.recv(1024).decode("utf8")
            if req == "unhook":
                record = keyboard.stop_recording() 
                con.sendall("Unhooked".encode("utf8"))
            req = con.recv(1024).decode("utf8")
            if req == "view":
                string = next(keyboard.get_typed_strings(record))
                con.sendall(string.encode("utf8"))
        if req == "shutdown":
            os.system("shutdown /s")

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