# EncryptedServer
This app is a combination of server and client which uses end to end encryption for maximum security.
To log on you must also provide a hashed md5 key or you will not be able to read and write messages or connect to the socket.
## To run server
Go to the messages file and run server.py. (make sure port 1000 is available)
This does not require any dependancies to run.
You will need the ip address of the server, or the public ip.
(you will need to expose port 1000)
## To connect client
Run the [client.py](https://github.com/IlhamIbrahimli/EncryptedServer/blob/main/client.py)
file and input a name, pass key (see later) and the ip of the server.

To change the key, go to  [line 23](https://github.com/IlhamIbrahimli/EncryptedServer/blob/main/Server/server.py).

![image](https://user-images.githubusercontent.com/78649705/232284204-b45e8bc0-3a60-4d58-a034-4649d173e70f.png)

The key is an md5 encrypted hash.
Remember the plaintext version inorder to give it to users.

Make sure that the 'Messages.txt' file exists in the directory.
Before running the client, run the pip command `pip install kivymd pycryptodome`
to make sure the dependancies are installed.
Now run the client and input your name, the ip address of the server and the unencrypted key.
## Usage
When you connect, the messages file will load all previous messages sent on the server previously.

### Future Plans
Add RSA instead of AES encryption
