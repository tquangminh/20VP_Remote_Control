import imp
from importlib.resources import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter.filedialog import askopenfile
import socket
import os,sys
import io
import tkinter as tk

import socket
import csv

from sklearn.metrics import top_k_accuracy_score

global HOST, PORT

window = Tk()
window.resizable(False, False) 
window.title('Process')

style = ttk.Style()
style.theme_use("clam")
txt_cl = "#F5DEB3"
frame1 = Frame(window)
frame1.pack()
  
can_show = Canvas(frame1,
bg = "#ffffff",
height = 330,
width = 390,
bd = 0,
highlightthickness = 0,
relief = "ridge")
can_show.pack(fill = "both", expand = True)
                
Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)

Fira_Sans10 = tkFont.Font(family='Fira Sans', size=10, weight=tkFont.BOLD)

def entry_clear_IP(e):
    if ip_entry.get() == "Enter IP":
        ip_entry.delete(0,END)

def connectSocket():
    HOST = ip_entry.get()
    PORT = 1239
    try:
        global cli 
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.connect((HOST, PORT))
        cli.sendall('Client'.encode("utf8"))
        cli.recv(1024)
        print("Connect to Server successfully")
    except:
        print("Connection Lost", "Server has disconnected")

def process():   
    cli.sendall("process".encode("utf8"))
    cli.recv(1024)

    win = Toplevel(window)
    my_canvas = Canvas(win,
    bg = "#ffffff",
    height = 360,
    width = 810,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")

    my_canvas.pack(fill = "both", expand = True) 
    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)

    my_canvas.grab_set()
    def on_closing():
        cli.sendall('process closing'.encode('utf8'))
        cli.recv(1024)
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_closing)

    def view():
        cli.sendall("processList".encode("utf8"))
        res = cli.recv(50000).decode("utf8")
        data = (csv.reader(res.split('\n')))
        data = list(data)
        data = [x for x in data if x]

        del data[0:2]
    
    
        my_tree.tag_configure('oddrow', background="#ffffff")
        my_tree.tag_configure('evenrow', background="#63cdda")

        global count
        count=0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))
            count += 1

    def kill():
        cli.sendall('kill'.encode("utf8"))
        res = cli.recv(50000).decode("utf8")
        req = input("Request: ")
        cli.sendall(req.encode("utf8"))
        res = cli.recv(1024).decode("utf8")

    def delete():
        for item in my_tree.get_children():
            my_tree.delete(item)

    def start():
        cli.sendall('start'.encode("utf8"))
        cli.recv(1024)
        req = input("Request: ")
        cli.sendall(req.encode("utf8"))
        res = cli.recv(1024).decode("utf8")
    
    viewBtn = Button(my_canvas, text="Xem",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= view)
    viewBtn.place(x=210, y=30, height=40, width=175)
    killBtn = Button(my_canvas, text="Kill",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= kill)
    killBtn.place(x=25, y=30, height=40, width = 175)
    delBtn = Button(my_canvas, text="Xóa",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= delete)
    delBtn.place(x=395, y=30, height=40, width=175)
    startBtn = Button(my_canvas, text="Start",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= start)
    startBtn.place(x=580, y=30, height=40, width=175)


    style.configure("Treeview", 
    	background="#D3D3D3",
    	foreground="black",
    	rowheight=25,
    	fieldbackground="#D3D3D3"
    	)
    # Change selected color
    style.map('Treeview', 
    	background=[('selected', '#D3D3D3')])

    # Create Treeview Frame
    tree_frame = Frame(win)
    tree_frame.place(x=15, y=100, height=234, width=751)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    global my_tree
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    # Pack to the screen
    my_tree.place(x=0, y=0, height=234, width = 734)

    #Configure the scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("Name Process", "ID Process", "Count Thread")

    # Formate Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Name Process", anchor=W, width=140)
    my_tree.column("ID Process", anchor=CENTER, width=100)
    my_tree.column("Count Thread", anchor=W, width=140)

    # Create Headings 
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Name Process", text="Name Process", anchor=W)
    my_tree.heading("ID Process", text="ID Process", anchor=CENTER)
    my_tree.heading("Count Thread", text="Count Thread", anchor=W)
        
    win.mainloop()

def app():   
    cli.sendall("app".encode("utf8"))
    cli.recv(1024)

    win = Toplevel(window)
    my_canvas = Canvas(win,
    bg = "#ffffff",
    height = 360,
    width = 810,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")

    my_canvas.pack(fill = "both", expand = True) 
    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)

    my_canvas.grab_set()
    def on_closing():
        cli.sendall('app closing'.encode('utf8'))
        cli.recv(1024)
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_closing)

    def view():
        cli.sendall("appList".encode("utf8"))
        res = cli.recv(50000).decode("utf8")
        data = (csv.reader(res.split('\n')))
        data = list(data)
        data = [x for x in data if x]

        del data[0:2]
    
        my_tree.tag_configure('oddrow', background="#ffffff")
        my_tree.tag_configure('evenrow', background="#63cdda")

        global count
        count=0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))
            count += 1

    def kill():
        cli.sendall('kill'.encode("utf8"))
        res = cli.recv(50000).decode("utf8")
        req = input("Request: ")
        cli.sendall(req.encode("utf8"))
        res = cli.recv(1024).decode("utf8")

    def delete():
        for item in my_tree.get_children():
            my_tree.delete(item)

    def start():
        cli.sendall('start'.encode("utf8"))
        cli.recv(1024)
        req = input("Request: ")
        cli.sendall(req.encode("utf8"))
        res = cli.recv(1024).decode("utf8")
    
    viewBtn = Button(my_canvas, text="Xem",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= view)
    viewBtn.place(x=210, y=30, height=40, width=175)
    killBtn = Button(my_canvas, text="Kill",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= kill)
    killBtn.place(x=25, y=30, height=40, width = 175)
    delBtn = Button(my_canvas, text="Xóa",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= delete)
    delBtn.place(x=395, y=30, height=40, width=175)
    startBtn = Button(my_canvas, text="Start",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= start)
    startBtn.place(x=580, y=30, height=40, width=175)


    style.configure("Treeview", 
    	background="#D3D3D3",
    	foreground="black",
    	rowheight=25,
    	fieldbackground="#D3D3D3"
    	)
    # Change selected color
    style.map('Treeview', 
    	background=[('selected', '#D3D3D3')])

    # Create Treeview Frame
    tree_frame = Frame(win)
    tree_frame.place(x=15, y=100, height=234, width=751)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    global my_tree
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    # Pack to the screen
    my_tree.place(x=0, y=0, height=234, width = 734)

    #Configure the scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("Name app", "ID app", "Count Thread")

    # Formate Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Name app", anchor=W, width=140)
    my_tree.column("ID app", anchor=CENTER, width=100)
    my_tree.column("Count Thread", anchor=W, width=140)

    # Create Headings 
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Name app", text="Name app", anchor=W)
    my_tree.heading("ID app", text="ID app", anchor=CENTER)
    my_tree.heading("Count Thread", text="Count Thread", anchor=W)
        
    win.mainloop()

def printScr():
    cli.sendall('printScreen'.encode("utf8"))
    image = cli.recv(500000)   
    # writing it to the disk using opencv
    with open('screenshot.jpg', "wb") as f:
        f.write(image) 

def keystroke():
    req = 'keystroke'
    cli.sendall(req.encode("utf8"))
    cli.recv(1024)
    #hook
    req = input('request: ')
    cli.sendall(req.encode("utf8"))
    cli.recv(1024)
    #unhook
    req = input('request: ')
    cli.sendall(req.encode("utf8"))
    cli.recv(1024)
    #view
    req = input('request: ')
    cli.sendall(req.encode("utf8"))
    string = cli.recv(1024).decode('utf8')
    print(string)
def shutdown():
    cli.sendall('shutdown'.encode("utf8"))
    cli.recv(1024)


ip_entry = Entry(frame1, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
ip_entry.place(x=20, y=40,width=250,height=25)
ip_entry.insert(0,"Enter IP")
ip_entry.bind("<FocusIn>", entry_clear_IP)

ip_btn = Button(frame1, text="Kết nối",font=("Fira", 10,'bold'), fg="#d78e8e",bd=0,command=connectSocket)
ip_btn.place(x=275,y=40, width = 95)

processBtn = Button(can_show, text="Process Running",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=process, wraplength=80)

processBtn.place(x=20, y=90, height=220, width=85)

runBtn = Button(can_show, text="App Running",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=app)

runBtn.place(x=110, y=90, height=70, width=160) 


prtBtn = Button(can_show, text="Chụp màn hình",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=printScr)

prtBtn.place(x=110, y=165, height=65, width=160)


keyBtn = Button(can_show, text="Keystroke",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=keystroke)

keyBtn.place(x=275, y=90, height=140, width=95)

shutDownBtn = Button(can_show, text="Tắt máy",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=shutdown)

shutDownBtn.place(x=110, y=235, height=75, width=210)


outBtn = Button(can_show, text="Thoát",font=Fira_Sans10,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=NONE)

outBtn.place(x=325, y=235, height=75, width=45)

can_show.mainloop()  