from kivymd.app import MDApp

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
import socket
import base64 
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad,unpad
from datetime import datetime
import threading
import select
import sys
import time
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
                data = sock.recv(131072)
                messages = messages + decrypt(data.decode(),key,iv).decode() + "\n"
                
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

class CheckAuth(MDApp):
    def updating(self,dt):
        global updateData
        global messages
        global sock
        global isUpdated
        sock.sendall("UpdateMessages".encode())
        updateData = sock.recv(131072)
        encryptedMessages = ""
        encryptedMessages += updateData.decode()

        while "Updated" not in encryptedMessages:
            updateData = sock.recv(131072)
            encryptedMessages += updateData.decode()
            print(encryptedMessages)
            if "Updated" in encryptedMessages:
                break

        encryptedMessagesList = encryptedMessages.split("\n")
        print(encryptedMessages)
        print(encryptedMessagesList)
        for i in encryptedMessagesList[:-1]:
            messages += decrypt(i,key,iv).decode() + "\n"
        self.sm.switch_to(self.s2)
        self.messagePrintOutArea.scroll_y = 0
        thread = thread1()
        thread.start()

       
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
        self.messagePrintOut.height = (messages.count("\n")+1) * 18
        self.messagePrintOut.text_size = (self.messagePrintOut.width * 0.98, self.messagePrintOut.height)
    def build(self):

        global isUpdated
        self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Orange"
        self.sm = MDScreenManager()
        self.s1 = MDScreen(name="Screen1")
        self.s2 = MDScreen(name="Screen2")
        global nameText
        global handshakeText
        global ipText
        global messages
        layout = MDGridLayout(cols=1)

        nameText = MDTextField(size_hint_y=None, height=30,multiline=False,hint_text="Name")
        layout.add_widget(nameText)
       
        handshakeText = MDTextField(size_hint_y=None, height=30,multiline=False,hint_text="Key")
        layout.add_widget(handshakeText)

        ipText = MDTextField(size_hint_y=None, height=30,multiline=False,hint_text="IP")
        layout.add_widget(ipText)
        
        btn = MDRaisedButton(text="Connect",size_hint_y=None, height=100)
        btn.bind(on_press=confirmAndConnect)
        layout.add_widget(btn)
        self.s1.add_widget(layout)
       
        MessageLayout = MDGridLayout(cols=1)
        self.messagePrintOutArea = MDScrollView(do_scroll_y=True)
        self.messagePrintOut = MDLabel(text=messages, size_hint=(None,None),width=Window.size[0])

        self.entry = MDTextField(size_hint_y=None, height=90,halign="left",hint_text="Enter Message",mode="rectangle",font_name="seguiemj")
        self.entry.bind(on_text_validate=self.sendMessage)
        Clock.schedule_interval(self.UPDATE,0.1)
        MessageLayout.add_widget(self.messagePrintOutArea)
        self.messagePrintOut.font_name = "seguiemj"
        self.messagePrintOut.font_size = 18
        self.messagePrintOutArea.add_widget(self.messagePrintOut)

        MessageLayout.add_widget(self.entry)
        self.s2.add_widget(MessageLayout)
        self.sm.add_widget(self.s1)
        self.sm.add_widget(self.s2)
        
        return self.sm
    def on_stop(self):
        sock.sendall("end".encode())
        time.sleep(0.1)
        sock.close()

      
    
auth = CheckAuth()
auth.run()

sys.exit()


