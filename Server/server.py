import sys
import socket
import threading
import time
import select
ClientList = []
data = 0
messageFile = open("Messages.txt","r+")
class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      
   def run(self):
      while True:
        accept()
def accept():
    currc, addr = sock.accept()

    handShake = currc.recv(32)
    
    if handShake.decode("utf-8") != "e10adc3949ba59abbe56e057f20f883e":
        currc.sendall("Tx2".encode())
        time.sleep(0.1)
        currc.close()
    else:
       ClientList.append(currc)
       ClientList[-1].sendall("Tx1".encode())
BLOCK_SIZE = 16
def update_message():
   messageFile.write(message.decode("utf-8") + "\n")
   messageFile.flush()
   messages = []
   print(message)
   for i in range(len(ClientList)):
      ClientList[i].sendall(message)
sock = socket.socket()
sock.bind(("0.0.0.0",1000))
sock.listen()
UpdatingCount = 0
thread1 = myThread(1,"AcceptThread")
thread1.start()
updatingThreadList = []
class updateThread(threading.Thread):
   def __init__(self,notifSock,file):
      threading.Thread.__init__(self)
      self.notifSock = notifSock
      self.file = file
   def run(self):
      self.file.seek(0)
      self.notifSock.sendall(self.file.read().encode())
      self.notifSock.sendall("Updated".encode())
      sys.exit()
while True:
   if len(ClientList) != 0:
      read_sockets, _, exception_sockets = select.select(ClientList, [], ClientList,1)
      for notified_socket in exception_sockets:
        ClientList.remove(notified_socket)
      for notified_socket in read_sockets:
         message = notified_socket.recv(131072)
         if message.decode() == "UpdateMessages":
            updateThread(notified_socket,messageFile).start()
         else:
            if message.decode() == "end" or message.decode() == "":
               ClientList.remove(notified_socket)
               notified_socket.close()
            else:
               update_message()
