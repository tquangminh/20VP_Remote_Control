import io, os,sys, socket, csv, datetime

from tkinter import *
import tkinter as tk
from tkinter import Tk, ttk, messagebox , filedialog as fd, font as tkFont
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image  

global HOST, PORT

window = Tk()
window.resizable(False, False) 
window.title('Remote Control')

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

global cli
cli = None

def entry_clear_IP(e):
    if ip_entry.get() == "Enter IP":
        ip_entry.delete(0,END)

def connectSocket():
    global cli
    if cli != None:
        messagebox.showerror('Error', 'Already connect to server')
        return
    HOST = ip_entry.get()
    PORT = 1239
    
    try:
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.connect((HOST, PORT))
        cli.sendall('Client'.encode("utf8"))
        cli.recv(1024)
        messagebox.showinfo('Status', 'Connect to Server successfully') 
        print("Connect to Server successfully")
    except:
        cli = None
        messagebox.showerror('Error', "Server has disconnected")

def process():   
    if cli == None:
        messagebox.showerror('Error', "Connect to server first")
        return

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
        def killf():
            cli.sendall('kill'.encode("utf8"))
            res = cli.recv(50000).decode("utf8")
            pid = pid_entry.get()
            if pid == '':
                messagebox.showerror('error', 'invalid id', parent = win3)
                cli.sendall('pid close'.encode('utf8'))
                return
            messagebox.showinfo('Status', 'Kill the process successfully', parent = win3)
            cli.sendall(pid.encode("utf8"))
            res = cli.recv(1024).decode("utf8")

        win3 = Toplevel(window)
        win3.title('Kill')

        def on_closing():
            win3.destroy()
            my_canvas.grab_set()        
        win3.protocol("WM_DELETE_WINDOW", on_closing)

        killProcess_canvas = Canvas(win3,
        bg = "#ffffff",
        height = 100,
        width = 360,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")

        killProcess_canvas.pack(fill = "both", expand = True) 
        killProcess_canvas.grab_set()

        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
        def entry_clear_ID(e):
            if pid_entry.get() == "Nhập ID":
                pid_entry.delete(0,END)

        pid_entry = Entry(killProcess_canvas, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
        pid_entry.place(x=20, y=40,width=250,height=25)
        pid_entry.insert(0,"Nhập ID")
        pid_entry.bind("<FocusIn>", entry_clear_ID)

        killBtn = Button(killProcess_canvas, text="Kill",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command= killf)
        killBtn.place(x=280, y=40, height=25, width = 60)
        killProcess_canvas.mainloop()

    def delete():
        for item in my_tree.get_children():
            my_tree.delete(item)

    def start():
        def startf():
            cli.sendall('start'.encode("utf8"))
            cli.recv(1024)
            appName = name_entry.get()
            if appName == '':
                messagebox.showerror('error', 'invalid name', parent = win4)
                cli.sendall('name close'.encode('utf8'))
                return
            messagebox.showinfo('Status', 'Start the app successfully', parent = win4)
            cli.sendall(appName.encode("utf8"))
            res = cli.recv(1024).decode("utf8")

        win4 = Toplevel(window)
        win4.title('Start')

        def on_closing():
            win4.destroy()
            my_canvas.grab_set()        
        win4.protocol("WM_DELETE_WINDOW", on_closing)

        startProcess_canvas = Canvas(win4,
        bg = "#ffffff",
        height = 100,
        width = 360,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")

        startProcess_canvas.pack(fill = "both", expand = True) 

        startProcess_canvas.grab_set()

        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
        
        def entry_clear_name(e):
            if name_entry.get() == "Nhập tên":
                name_entry.delete(0,END)

        name_entry = Entry(startProcess_canvas, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
        name_entry.place(x=20, y=40,width=250,height=25)
        name_entry.insert(0,"Nhập tên")
        name_entry.bind("<FocusIn>", entry_clear_name)
        
        startBtn = Button(startProcess_canvas, text="Start",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command= startf)
        startBtn.place(x=280, y=40, height=25, width = 60)
        startProcess_canvas.mainloop()

    
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
    if cli == None:
        messagebox.showerror('Error', "Connect to server first")
        return

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
    win.title('App')
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
        def killf():
            cli.sendall('kill'.encode("utf8"))
            res = cli.recv(1024).decode("utf8")
            pid = pid_entry.get()
            if pid == '':
                messagebox.showerror('error', 'invalid id', parent = win3)
                cli.sendall('pid close'.encode('utf8'))
                return
            messagebox.showinfo('Status', 'Kill the app successfully', parent = win3)
            cli.sendall(pid.encode("utf8"))
            res = cli.recv(1024).decode("utf8")

        win3 = Toplevel(window)
        win3.title('Kill')
        def on_closing():
            win3.destroy()
            my_canvas.grab_set()        
        win3.protocol("WM_DELETE_WINDOW", on_closing)

        killProcess_canvas = Canvas(win3,
        bg = "#ffffff",
        height = 100,
        width = 360,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")

        killProcess_canvas.pack(fill = "both", expand = True) 
        killProcess_canvas.grab_set()

        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
        def entry_clear_ID(e):
            if pid_entry.get() == "Nhập ID":
                pid_entry.delete(0,END)

        pid_entry = Entry(killProcess_canvas, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
        pid_entry.place(x=20, y=40,width=250,height=25)
        pid_entry.insert(0,"Nhập ID")
        pid_entry.bind("<FocusIn>", entry_clear_ID)

        killBtn = Button(killProcess_canvas, text="Kill",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command= killf)
        killBtn.place(x=280, y=40, height=25, width = 60)
        killProcess_canvas.mainloop()

    def delete():
        for item in my_tree.get_children():
            my_tree.delete(item)

    def start():
        def startf():
            cli.sendall('start'.encode("utf8"))
            cli.recv(1024)
            appName = name_entry.get()
            if appName == '':
                messagebox.showerror('error', 'invalid name', parent = win4)
                cli.sendall('name close'.encode('utf8'))
                return
            messagebox.showinfo('Status', 'Start the app successfully',parent = win4)
            cli.sendall(appName.encode("utf8"))
            res = cli.recv(1024).decode("utf8")

        win4 = Toplevel(window)
        win4.title('Start')
        def on_closing():
            win4.destroy()
            my_canvas.grab_set()        
        win4.protocol("WM_DELETE_WINDOW", on_closing)
        startProcess_canvas = Canvas(win4,
        bg = "#ffffff",
        height = 100,
        width = 360,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")

        startProcess_canvas.pack(fill = "both", expand = True) 

        startProcess_canvas.grab_set()

        Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
        
        def entry_clear_name(e):
            if name_entry.get() == "Nhập tên":
                name_entry.delete(0,END)

        name_entry = Entry(startProcess_canvas, font=("Courier New", 11),fg="#303952",bg = "#ebc6c6", bd=0)
        name_entry.place(x=20, y=40,width=250,height=25)
        name_entry.insert(0,"Nhập tên")
        name_entry.bind("<FocusIn>", entry_clear_name)
        
        startBtn = Button(startProcess_canvas, text="Start",font=Fira_Sans,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command= startf)
        startBtn.place(x=280, y=40, height=25, width = 60)
        startProcess_canvas.mainloop()
    
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
    if cli == None:
        messagebox.showerror('Error', "Connect to server first")
        return

    win1 = Toplevel(window)
    prt_canvas = Canvas(win1,
    bg = "#ffffff",
    height = 400,
    width = 550,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
    win1.title('Print Scrren')
    win1.grab_set()
    prt_canvas.pack(fill = "both", expand = True) 

    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
    global imgbyte
    imgbyte = ''

    def prt():
        global imgbyte
        cli.sendall('printScreen'.encode("utf8"))
        imgbyte = cli.recv(700000)   
        image = Image.open(io.BytesIO(imgbyte))
        imageresize  = image.resize((480, 270),Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(imageresize)
        panel = Label(prt_canvas, image = img, relief = GROOVE)
        panel.place(x = 30, y = 30)
        panel.mainloop()
    
    def saveImg():
        if imgbyte == '':
            messagebox.showinfo('Status','No Image', parent = win1)
            return
        dir = ''
        dir = fd.askdirectory(parent=win1)
        if dir == '':
            return
        current_time = str(datetime.datetime.now()).replace(' ','_').replace('.','_').replace(':',"_").replace('-',"_")
        with open(os.path.basename(dir+'/'+current_time+'.jpg'), "wb") as f:
            f.write(imgbyte) 
        messagebox.showinfo('Status','Saved', parent = win1)
    
    PrtScBtn = Button(prt_canvas, text="Chụp",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= prt)
    PrtScBtn.place(x=30, y=315, height=40, width = 230)

    saveBtn = Button(prt_canvas, text="Lưu",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= saveImg)
    saveBtn.place(x=280, y=315, height=40, width=230)
    prt_canvas.mainloop()
    win1.mainloop()

def keystroke():
    if cli == None:
        messagebox.showerror('Error', "Connect to server first")
        return

    keystrokeLs = []
    cli.sendall('keystroke'.encode("utf8"))
    cli.recv(1024)
    global hookcheck
    hookcheck = 0

    def hook():
        global hookcheck
        if hookcheck == 1:
            messagebox.showerror('status', 'Already hooked', parent = win2)
            return        
        cli.sendall('hook'.encode("utf8"))
        cli.recv(1024)
        hookcheck = 1
        messagebox.showinfo('status', 'hooked', parent = win2)       
    def unhook():
        global hookcheck
        if hookcheck != 1:
            messagebox.showerror('status', 'Havent hooked', parent = win2)
            return
        global keystrokeLS
        cli.sendall('unhook'.encode("utf8"))
        res = cli.recv(1024).decode('utf8')
        messagebox.showinfo('status', 'unhooked',parent = win2)
        hookcheck = 0
        if res == 'nothing hook':
            return
        keystrokeLs.append(res)
    def view():
        global keystrokeLS
        for i in range(len(keystrokeLs)):
            keystrokeStrListBox.insert(END, keystrokeLs.pop(0))
    def clear():
        keystrokeStrListBox.delete(first = 0, last = keystrokeStrListBox.size())
    
    win2 = Toplevel(window)
    win2.title('KeyStroke')
    stroke_canvas = Canvas(win2,
    bg = "#ffffff",
    height = 360,
    width = 810,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
    stroke_canvas.pack(fill = "both", expand = True) 
    
    stroke_canvas.grab_set()
    def on_closing():
        cli.sendall('keystroke closing'.encode('utf8'))
        cli.recv(1024)
        win2.destroy()
    win2.protocol("WM_DELETE_WINDOW", on_closing)

    Fira_Sans = tkFont.Font(family='Fira Sans', size=13, weight=tkFont.BOLD)
    scrollbar = Scrollbar(stroke_canvas)
    keystrokeStrListBox = Listbox(stroke_canvas,yscrollcommand = scrollbar.set)
    keystrokeStrListBox.place(x=15, y=100, height=234, width=751)
    scrollbarX = Scrollbar(keystrokeStrListBox,orient = HORIZONTAL)
    scrollbarY = Scrollbar(keystrokeStrListBox,orient = VERTICAL)

    keystrokeStrListBox.configure(yscrollcommand = scrollbarY.set)
    keystrokeStrListBox.configure(xscrollcommand=scrollbarX.set)
       
    scrollbarY.config(command = keystrokeStrListBox.yview)
    scrollbarY.pack( side = RIGHT, fill = Y)

    scrollbarX.config(command = keystrokeStrListBox.xview)
    scrollbarX.pack(side = BOTTOM, fill = X)

    hookBtn = Button(stroke_canvas, text="Hook",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= hook)
    hookBtn.place(x=25, y=30, height=40, width = 175)

    unHookBtn = Button(stroke_canvas, text="Unhook",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= unhook)
    unHookBtn.place(x=210, y=30, height=40, width=175)

    prBtn = Button(stroke_canvas, text="In phím",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= view)
    prBtn.place(x=395, y=30, height=40, width=175)

    delBtn = Button(stroke_canvas, text="Xóa",font=Fira_Sans,borderwidth=2,bg="#63cdda",fg = "#FFFFFF", command= clear)
    delBtn.place(x=580, y=30, height=40, width=175)
    win2.mainloop()


def shutdown():
    if cli == None:
        messagebox.showerror('Error', "Connect to server first")
        return
    cli.sendall('shutdown'.encode("utf8"))
    cli.close()
    messagebox.showinfo("Status", 'Shutdown successfully')

def out():
    if cli != None:
        cli.close()
    window.destroy()

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

outBtn = Button(can_show, text="Thoát",font=Fira_Sans10,borderwidth=0,bg="#63cdda",fg = "#FFFFFF", command=out)
outBtn.place(x=325, y=235, height=75, width=45)

can_show.mainloop()  