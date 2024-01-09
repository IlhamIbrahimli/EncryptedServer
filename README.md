# EncryptedServer
This app is a combination of server and client which uses end to end encryption for maximum security.
To log on you must also provide a hashed md5 key or you will not be able to read and write messages or connect to the socket.
## To run server
Go to the "Server" folder in the latest release and run server.exe. (make sure port 1000 is available)
You will need the ip address of the server, or the public ip.
(you will need to expose port 1000)
When starting the server you will be asked to enter a hashed md5 pass key. To generate the pass key run md5hasher.exe and
enter the plaintext version (the one which will be given to users).
## To connect client
Run client.exe which can be found in the "Client" folder in the latest release and then input a name, pass key (see later) and the ip of the server.


Make sure that the 'Messages.txt' file exists in the server directory.
Now run the client and input your name, the ip address of the server and the unencrypted key.
## Usage
When you connect, the messages file will load all previous messages sent on the server previously.

### Future Plans
Add RSA instead of AES encryption
