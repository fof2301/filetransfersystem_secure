#to ask a user for a file and then decryot the given file 
#and replace it in the given folder to make the file encrypted
#using tkinter to graphically ask the user for the file
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
from calc import encoder as enc
from calc import decoder as dec
import http.server
import socketserver
import threading
import requests
from pathlib import Path


class decrypterClass():
    def __init__(self,file,fpath):
        self.file=file
        self.fpath=fpath
    def decrypt(self):
         dec(self.file,self.fpath)

class encrypterClass():
    def __init__(self,file,fpath):
        self.file=file
        self.fpath=fpath
    def encrypt(self):
        enc(self.file,self.fpath)

class senderClass():
    def __init__(self,file):
        self.file=file
    def start_web_server(self):
        class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                print(str(Path.cwd()))
                super().__init__(*args,directory=str(Path.cwd())+"/secrets", **kwargs)
    
            def log_message(self, format, *args):
                return
    
        def serve_forever():
            server.serve_forever()
    
        # Create a socket server with the specified port and request handler
        server = socketserver.TCPServer(("", 8000), MyRequestHandler)
        print(f"Server started on port {8000}")
        
        # Start the server on a separate thread
        thread = threading.Thread(target=serve_forever)
        thread.start()
        
        # Return the server and thread objects
        return server, thread

class reciever_class():
    def __init__(self,file:str,ip:str):
        self.file=file
        self.ip=ip
    def recieve_file(self):
        print("server opened")
        # URL of the image to be downloaded is defined as url
        try:
                url = "http://"+self.ip+":8000/"+self.file
                r = requests.get(url) # create HTTP response object
                print(str(r))
        except:
            FileNotFoundError
        # # send a HTTP request to the server and save
        # # the HTTP response in a response object called r
        with open(str(Path.cwd())+"/"+"tmp_encrypted.png.png",'wb') as f:
        #     # Saving received content as a png file in
        #     # binary format
        
        #     # write the contents of the response (r.content)
            # to a new file in binary mode.
            f.write(r.content)    
        dec("tmp_encrypted.png.png",str(Path.cwd())+"/secrets/")         

class filehandler(encrypterClass,decrypterClass,senderClass):
    def __init__(self,file,fpath):
        self.file=file
        self.fpath=str(Path.cwd())+"/secrets"
    def encrypt(self):
        enc(self.file,self.fpath)
        print("file encryption success")
    def decrypt(self):
        dec(self.file,self.fpath)
        print("file decryption success")
    def send(self):
        print("here")
        filehandler.encrypt(self)
        s1=senderClass(self.file)
        server, thread = s1.start_web_server()
        print("server inititated")   
      
        
        

# create the root window
root = tk.Tk()
root.title('💀 cHoOsE a FiLe 💀')
root.resizable(False, False)
root.geometry('350x215')
print(Path.cwd())
bg = PhotoImage( file = str(Path.cwd())+"/background_image.png")
  
# Show image using label
label1 = Label( root,image=bg)
label1.place(x = 0,y = 0)

filepath=""

def select_file_encode():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    global filepath
    filepath=filename
    print(filepath)
    showinfo(
        title='Selected File',
        message=filename
    )
    finalpath=filepath.rsplit("/",1)
    file1=encrypterClass(filepath,finalpath[0])
    file1.encrypt()
    print("func called")

def select_file_decode():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    global filepath
    filepath=filename
    print(filepath)
    showinfo(
        title='Selected File',
        message=filename
    )
    finalpath=filepath.rsplit("/",1)
    file2=decrypterClass(filepath,finalpath[0])
    file2.decrypt()
    print("func called")    

def web_server_initiate():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    global filepath
    filepath=filename
    print(filepath)
    showinfo(
        title='Selected File',
        message=filename
    )
    file3 = filehandler(filepath,filepath)
    file3.send()
    print("file encrypted and server opened")


def recieve_file():
    ip=get_input()
    file4 = reciever_class("tmp_encrypted.png.png",ip)
    file4.recieve_file()


def get_input():
    input_text = entry.get()
    print(input_text)
    return input_text  
    

#button
button1 = Button(
    root,
    text='Encrypt File',
    command=select_file_encode,
    width=10
)
button2 = Button(
    root,
    text='Decrypt File',
    command=select_file_decode,
    width=10
)
button3 = Button(
    root,
    text='Send File',
    command=web_server_initiate,
    width=10
)
button4 = Button(
    root,
    text='Recieve File',
    command=recieve_file,
    width=10
)

button5 = Button(
    root, 
    text="Sender's IP", 
    command=get_input)

# entry = tk.Entry(root)
# entry.pack()

# Create a button to retrieve the input text
entry = tk.Entry(root)

# Configuring the grid layout
root.columnconfigure(0, weight=1)  # Center align the buttons horizontally

# Placing the buttons on the grid
button1.grid(row=0, column=0, padx=10, pady=10)
button2.grid(row=0, column=1, padx=10, pady=10)
button3.grid(row=1, column=0, padx=10, pady=10)
button4.grid(row=1, column=1,padx=10, pady=10 )

entry.grid(row=2, column=1,padx=10, pady=5)



# run the application
root.mainloop()


