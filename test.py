import imp
from importlib.resources import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image  
import socket
import os,sys
import io
import tkinter as tk


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

def process(): 
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

    killBtn = Button(my_canvas, text="Kill",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
    killBtn.place(x=25, y=30, height=40, width = 175)
    viewBtn = Button(my_canvas, text="Xem",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
    viewBtn.place(x=210, y=30, height=40, width=175)
    delBtn = Button(my_canvas, text="Xóa",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
    delBtn.place(x=395, y=30, height=40, width=175)
    startBtn = Button(my_canvas, text="Start",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
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

    # Add Data
    data = [
    	["Notepad", 100, 1],
    	["Notepad", 200, 1],
    	["Notepad", 300, 1],
    	["Notepad", 400, 1],
    	["Notepad", 500, 1],
    	["Notepad", 600, 1],
    	["Notepad", 700, 1],
    	["Notepad", 800, 1],
    	["Notepad", 900, 1],
    	["Notepad", 100, 1],
    	["Notepad", 110, 1],
            ]

    
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


def prtsc(): 
    win1 = Toplevel(window)

    prt_canvas = Canvas(win1,
    bg = "#ffffff",
    height = 400,
    width = 550,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")

    prt_canvas.pack(fill = "both", expand = True) 


    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)


    image = Image.open(r"C:\Users\Asus\Pictures\Feedback\Untitled.jpg")
    imageresize  = image.resize((480, 270),Image.Resampling.LANCZOS)

    img = ImageTk.PhotoImage(imageresize)
    
    panel = Label(prt_canvas, image = img, relief = GROOVE)
    
    panel.place(x = 30, y = 30)
    PrtScBtn = Button(prt_canvas, text="Chụp",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
    PrtScBtn.place(x=30, y=315, height=40, width = 230)

    saveBtn = Button(prt_canvas, text="Lưu",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= NONE)
    saveBtn.place(x=280, y=315, height=40, width=230)
    win1.mainloop()
    prt_canvas.mainloop()
def entry_clear_IP(e):
        if ip_entry.get() == "Enter IP":
            ip_entry.delete(0,END)

ip_entry = Entry(can_show, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
ip_entry.place(x=20, y=40,width=250,height=25)
ip_entry.insert(0,"Enter IP")
ip_entry.bind("<FocusIn>", entry_clear_IP)

ip_btn = Button(can_show, text="Kết nối",font=("Fira", 10,'bold'), fg="#d78e8e",bd=0,command=NONE)
ip_btn.place(x=275,y=40, width = 95)

processBtn = Button(can_show, text="Process Running",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=process, wraplength=80)

processBtn.place(x=20, y=90, height=220, width=85)

runBtn = Button(can_show, text="App Running",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=NONE)

runBtn.place(x=110, y=90, height=70, width=160) 


prtBtn = Button(can_show, text="Chụp màn hình",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=prtsc)

prtBtn.place(x=110, y=165, height=65, width=160)


keyBtn = Button(can_show, text="Keystroke",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=NONE)

keyBtn.place(x=275, y=90, height=140, width=95)

shutDownBtn = Button(can_show, text="Tắt máy",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=NONE)

shutDownBtn.place(x=110, y=235, height=75, width=210)


outBtn = Button(can_show, text="Thoát",font=Fira_Sans10,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=NONE)

outBtn.place(x=325, y=235, height=75, width=45)

can_show.mainloop()  




