# EncryptedServer

This app is a combination of server and client which uses end to end encryption for maximum security.
To log on you must also provide a hashed md5 key or you will not be able to read and write messages or connect to the socket.

# To change the md5 encryption key
1. Open server.py.
2. Go to line 23.
3. You should see a hash.
4. Edit this with an md5 hash of your choosing.


![image](https://user-images.githubusercontent.com/78649705/232284204-b45e8bc0-3a60-4d58-a034-4649d173e70f.png)

This app can work on both public and private IP's.
To use a public IP you need to access the router's settings where the server.py is running and port forward port 1000.
