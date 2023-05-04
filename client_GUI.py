import tkinter as tk
from tkinter import ttk
from socket import *
import threading

#   GUI - START

ui_blue = '#3498db'
ui_silver = '#bdc3c7'

class CHAT:
    def __init__(self, address):
        
        if (address == '1'): address = 'localhost'
        server_port = 12000 
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((address, server_port))
        print(f'Connected to server at {address}:{server_port}')

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        
        self.root = tk.Tk()
        self.root.geometry('400x600')
        self.root.title('Chatroom')
        self.root.resizable(False, False)
        self.root.configure(background='white')
        
        self.container = tk.Frame(self.root)
        self.container.columnconfigure(0, weight= 1)
        self.container.rowconfigure(0, weight= 1)
        self.container.rowconfigure(1, weight= 5)
        self.container.rowconfigure(2, weight= 1)
        
        #       The bubbles go here.
        canvas_container = tk.Frame(self.container)
        canvas_container.grid(row=1, column=0, sticky= 'news')

        self.canvas = tk.Canvas(canvas_container, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_container = tk.Frame(self.container)
        scrollbar_container.grid(row=1, column=0, sticky= 'nse')
        
        scrollbar = ttk.Scrollbar(scrollbar_container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.chat, anchor=tk.NW, width=385)

        #       End of chat region set up.
        
        #       Header and input here.
        
        header = tk.Frame(self.container, bg= ui_blue, height= 30, highlightthickness= 0, borderwidth= 0)
        
        addressLabel = tk.Label(header, bg= ui_blue, text=f'Connected to {address}', font=('Arial', 10), fg= 'white', height= 2)
        addressLabel.pack(fill= tk.Y, expand= True)
        
        inputFrame = tk.Frame(self.container, bg= ui_silver, height= 120, highlightthickness= 0, borderwidth= 0)
        
        self.inputEntry = tk.Text(inputFrame, font=('Arial',11),height=  2, width= 35, relief= 'flat', borderwidth= 0)
        self.inputEntry.pack(side= 'left', padx= 5, pady= 10)
        
        send = tk.Button(inputFrame, bg= ui_blue, fg='white', font=('Arial', 9), text='SEND', relief= 'flat', borderwidth= 0, activebackground='#2980b9', activeforeground= 'white', command=self.sendMessage)
        send.pack(fill= 'both', expand= True, pady= 10, padx= 1)
        
        header.grid(row=0,column=0,sticky='new', padx= 0, pady=0)
        inputFrame.grid(row=2,column=0,sticky='ews', padx=0, pady=0)
        
        #       Adding the main container to the root.
        self.container.pack(fill = 'both', expand= True)
        
        self.root.bind('<Return>', self.onKeypress)
        self.root.bind_all("<MouseWheel>", self.onMousewheel)
        self.root.mainloop()
    
    def outBubble(self, message):
        bubble = tk.Label(self.chat, bg= ui_silver, text=message, font=('Arial', 11))
        bubble.pack(side='top', padx=10, pady=5, anchor='se', ipadx= 8, ipady= 4)
        
    def inBubble(self, message):
        bubble = tk.Label(self.chat, bg= ui_blue, fg= 'white', text=message, font=('Arial', 11))
        bubble.pack(side='top', padx=8, pady=4, anchor='sw', ipadx= 8, ipady= 4)
        
    def sendMessage(self, keypress=False):
        
        if keypress is False:
            message = self.inputEntry.get('1.0','end-1c')
        else:
            message = self.inputEntry.get('1.0','end-2c') 
        
        self.inputEntry.delete('1.0', 'end')
        self.outBubble(message)
        self.socket.send(message.encode())
        
    def onKeypress(self, event):
        self.sendMessage(True)
        
    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion= self.canvas.bbox("all"))
    
    def onMousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
        
    def receive_messages(self):
        
        while True:
        
            data = self.socket.recv(1024)
            print("Them: ", data.decode())
            
            if not data:
                break
        
            self.inBubble(data.decode())

        
#   GUI - FINISH

def redirect():
        
    temp = inputfield.get()
    if temp != '': address = temp
    else: address = '1'
        
    menu.destroy()
    CHAT(address)

menu = tk.Tk()
menu.geometry('400x400')
menu.title('MENU')
menu.resizable(False, False)
menu.configure(background='white')
        
container = tk.Frame(menu, bg= 'white')
label1 = tk.Label(container, text='Input the server IP or hostname:', font=('Arial', 12), bg= 'white')
label1.pack(pady= 2)
label2 = tk.Label(container, text='Leave blank for localhost.', font=('Arial', 9), bg= 'white', fg='gray')
label2.pack()
                
inputfield = tk.Entry(container, font=('Arial', 11), bg= 'white', border= 1, relief= 'solid', justify= 'center')
inputfield.pack(pady= 15, ipadx=5, ipady=5)
        
confirm = tk.Button(container, bg= ui_blue, fg='white', font=('Arial', 11), text='CONNECT', relief= 'flat', borderwidth= 0, activebackground='#2980b9', activeforeground= 'white', command=redirect)
confirm.pack(ipadx=10, ipady=5, pady=10)
        
container.pack(pady=100)
        
menu.mainloop()