from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import base64 
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad,unpad
from datetime import datetime
import threading
import select
import sys

key = "fhak1x7d9ujsfysd"
iv =  'k1809vcqhpb7jnbd'.encode('utf-8')
name = ""
handshake = ""
ip = ""
messages = ""
def encrypt(data,key,iv):
    data= pad(data.encode(),16)
    cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
    return base64.b64encode(cipher.encrypt(data))
def decrypt(enc,key,iv):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)

class thread1(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)

      
    def run(self):
        global messages
        
        while True:
            
            ready = select.select([sock], [], [], )
            if ready[0]:
                data = sock.recv(4096)
                
                messages = messages + decrypt(data.decode("utf-8"),key,iv).decode() + "\n"
def confirmAndConnect(instance):
    global name
    global handshake
    global updatedmessages
    global sock
    global data
    global messages
    name = nameText.text
    handshake = handshakeText.text
    ip = ipText.text
    updatedmessages = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = ""
    sock.connect((ip,1000))
    sock.sendall(MD5.new(handshake.encode()).hexdigest().encode())
    a = sock.recv(3)
    if a.decode() == "Tx2":
        sys.exit()
    else:
        Clock.schedule_once(auth.updating,0.1)
        
isUpdated = False

class CheckAuth(App):
    def updating(self,dt):
        global updateData
        global messages
        global sock
        global isUpdated
        sock.sendall("UpdateMessages".encode())
        updateData = sock.recv(4096)

        if updateData.decode() != "Updated":
            messages = messages + decrypt(updateData.decode("utf-8"),key,iv).decode().strip() + "\n"
            while updateData.decode() != "Updated":
                updateData = sock.recv(4096)
                print(updateData)
                if updateData.decode() == "Updated":
                    self.sm.switch_to(self.s2)
                    thread = thread1()
                    thread.start()
                    break
                else:
                    messages = messages + decrypt(updateData.decode("utf-8"),key,iv).decode() + "\n"
            print(messages)
       
    def sendMessage(self,widge): 
        
        now = datetime.now()
        current_time = now.strftime("%D-%H:%M:%S")
        message = name + ":" + current_time + ">" + self.entry.text
        message = encrypt(message,key,iv)
        self.entry.text = ""
        sock.sendall(message)                
    def UPDATE(self,dt):
        global messages
        self.messagePrintOut.text = ""
        self.messagePrintOut.text = messages
    def build(self):
        global isUpdated
        self.sm = ScreenManager()
        self.s1 = Screen(name="Screen1")
        self.s2 = Screen(name="Screen2")
        global nameText
        global handshakeText
        global ipText
        global messages
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Name',size_hint_y=None, height=30,halign="left"))
        nameText = TextInput(size_hint_y=None, height=30,multiline=False)
        layout.add_widget(nameText)
        layout.add_widget(Label(text='Key',size_hint_y=None, height=30,halign="left"))
        handshakeText = TextInput(size_hint_y=None, height=30,multiline=False)
        layout.add_widget(handshakeText)
        layout.add_widget(Label(text='IP',size_hint_y=None, height=30,halign="left"))
        ipText = TextInput(size_hint_y=None, height=30,multiline=False)
        layout.add_widget(ipText)
        
        btn = Button(text="Connect",size_hint_y=None, height=100)
        btn.bind(on_press=confirmAndConnect)
        layout.add_widget(btn)
        self.s1.add_widget(layout)
       
        MessageLayout = GridLayout(cols=1)
        messagePrintOutArea = ScrollView(do_scroll_y=True)
        self.messagePrintOut = Label(text=messages,size_hint=(None,None),width=Window.size[0],height=10000,halign="left", valign="top",text_size=(Window.size[0],10000))
        self.entry = TextInput(size_hint_y=None, height=90,halign="left")
        btn2 = Button(text="send",size_hint_y=None, height=50)
        btn2.bind(on_press=self.sendMessage)
        Clock.schedule_interval(self.UPDATE,0.1)
        MessageLayout.add_widget(messagePrintOutArea)
        messagePrintOutArea.add_widget(self.messagePrintOut)
        MessageLayout.add_widget(self.entry)
        MessageLayout.add_widget(btn2)
        self.s2.add_widget(MessageLayout)
        self.sm.add_widget(self.s1)
        self.sm.add_widget(self.s2)
        
        return self.sm


      
    
auth = CheckAuth()
auth.run()
sock.sendall("end".encode())
sock.close()
sys.exit()


