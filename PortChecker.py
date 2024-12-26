import tkinter as tk
from tkinter import PhotoImage
import threading
import socket

root = tk.Tk()
root.title("Window")

portlimit = 5000

def WriteToConsole(txt):
    MainConsole.insert(tk.END,f"CONSOLE: {txt}\n")
    
class Font:
    
    class Fonts:
    
        ComicSans = "Comic Sans MS"
        Arial = "Arial"
        Courier = "Courier"
    
    class Formatting:
        
        class Italic:
        
            Bold = "italic bold"
            Normal = "italic normal"
        
        class NonItalic:
        
            Bold = "bold"
            Normal = "normal"
    
class Errors:
    Errors = {
        0:"PORT NOT SUPPORTED",
        1:"PORT DOESN'T EXIST",
        2:"NOTHING ENTERED"
        }

class TKDisplay:

    def DisplayText(roott,size,fon="Arial",fonttype="bold",colorfg="Black",colorbg=None,xpad=0,ypad=0):
        
        Text = tk.Text(
            master=roott,
            font=(fon,size,fonttype),
            fg= colorfg,
            )
        if colorbg:
            Text.config(bg=colorbg)
        
        Text.pack(padx=xpad,pady=ypad)
        
        
        return Text
    
    def DisplayTextButton(roott,txt,size,fon="Arial",fonttype="bold",colorfg="Black",colorbg=None,xpad=0,ypad=0,cmd=None):
       
        Text = tk.Button(roott,
                         text=txt,
                         font=(fon,size,fonttype),
                         fg=colorfg,
                         )
        if colorbg:
            Text.config(bg=colorbg)
        Text.pack(padx=xpad,pady=ypad)
        if cmd:
            Text.config(command=cmd)
        return Text
    
    def DisplayTextBox(roott,size,fon="Arial",fonttype="bold",colorfg="Black",colorbg=None,xpad=0,ypad=0):
        
        Text = tk.Entry(roott,
                        font=(fon,size,fonttype),
                        fg=colorfg,
                        )
        if colorbg:
            Text.config(bg=colorbg)
        Text.pack(padx=xpad,pady=ypad)
        return Text
    
    def DisplayTextLabel(roott,txt,size,fon="Arial",fonttype="bold",colorfg="Black",colorbg=None,xpad=0,ypad=0):
            
            Text = tk.Label(
                master=roott,
                text=txt,
                font=(fon,size,fonttype),
                fg= colorfg,
                )
            if colorbg:
                Text.config(bg=colorbg)
            
            Text.pack(padx=xpad,pady=ypad)
            
            
            return Text
        
def CreateNewClient():
    
    Root = tk.Tk()
    Root.config(bg="Black")
    EntryBox = TKDisplay.DisplayTextBox(
        Root,
        30,
        Font.Fonts.Courier,
        Font.Formatting.NonItalic.Normal,
        colorfg="#20C20E",
        colorbg="Black",
    )
    
    EntryBox.config(justify="center")
    
    def cp():
        port = EntryBox.get()
           
        if port == "":
            WriteToConsole("ERRORID:3")
            return {"ERRORID":3}
        
        port = int(EntryBox.get())
        
        if int(port) > portlimit:
            return {"ERRORID":0}
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1',port))
        if result == 0:
            WriteToConsole(f"Port {port} OPEN")
        else:
            WriteToConsole(f'port {port} CLOSED, connect_ex returned: '+str(result))
        sock.close()
    
    def CheckPort():
        
        threading.Thread(None,cp).start()
        
        
    def cps():
        
        port = EntryBox.get()
        
        if port == "":
            
                WriteToConsole("ERRORID:3")
                return {"ERRORID":3}
        
        if port.count("-") == 1:
            table = port.split("-")
            port = int(table[1])
            
            if port > portlimit:
                
                WriteToConsole("ERRORID:0")
                return {"ERRORID":0}
            
            WriteToConsole(f"Starting search from {table[0]}-{table[1]}")
            
            while port > int(table[0]):

                sock = socket.socket()
                sock.settimeout(0.001)
                result = sock.connect_ex(('127.0.0.1',port))
                if result == 0:
                    WriteToConsole(f"Port {str(port)} OPEN")
                sock.close()
                
                port -= 1
            
            WriteToConsole(f"Finished search from {table[0]}-{table[1]}")
            
            return
        
        else:
            
            port = int(port)

        WriteToConsole(f"Searching from 0-{str(port)}")
        
        if port > portlimit:
            return {"ERRORID":0}
        
        while port > 0:

            sock = socket.socket()
            sock.settimeout(0.001)
            result = sock.connect_ex(('127.0.0.1',port))
            if result == 0:
                WriteToConsole(f"Port {str(port)} OPEN")
            sock.close()
            
            port -= 1
        
        WriteToConsole(f"Finished search from 0-{str(port)}")
        
    def CheckPorts():
        threading.Thread(None,cps,None).start()
        
        
    StartButton = TKDisplay.DisplayTextButton(
        Root,
        "Check Port",
        15,
        Font.Fonts.ComicSans,
        Font.Formatting.NonItalic.Normal,
        cmd=CheckPort,
        colorfg="#20C20E",
        colorbg="Black",
        )
    
    DoPortsButton = TKDisplay.DisplayTextButton(
        Root,
        "Check All Ports from Number to 0",
        15,
        Font.Fonts.ComicSans,
        Font.Formatting.NonItalic.Normal,
        cmd=CheckPorts,
        colorfg="#20C20E",
        colorbg="Black",
        )
    
    Root.mainloop()
    
MainConsole = TKDisplay.DisplayText(root,10,colorfg="#20C20E",colorbg="Black",)
MainConsole.config(height=20)

MainButton = TKDisplay.DisplayTextButton(root,"Create New Client",20,Font.Fonts.Courier,Font.Formatting.NonItalic.Bold,cmd=CreateNewClient,colorfg="#20C20E",colorbg="Black",)

WriteToConsole("WELCOME TO THE CONSOLE, YOU MAY TYPE IN THE CLIENT A SINGLE NUMBER FOR PORT CHECKING 0 TO THAT NUMBER or TYPE IN #-# FOR PORTCHECKING THE NUMBER TO THE NUMBER")

root.config(bg="Black")

root.mainloop()
