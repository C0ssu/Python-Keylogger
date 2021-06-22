import socket
port = "4040"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), port))
s.listen(1)
connection = False
print("Making a socket was succesful! \n")
print("Waiting for connections...")
while True:
    if connection != True:
        try:
            connectorsocket, address = s.accept()
            print(f"A user with ip: {address} has connected! \n")
            connectorsocket.send(bytes('SERVER: You have connected to the server!', 'utf-8'))
            connection = True
        except:
            print("Error occured")
            connection = False
        else:
            print(f"Receiving data from {address} \n")
    else:
        try:
            connectorsocket.send(bytes('test', 'UTF-8'))
            data = connectorsocket.recv(1024)
        except:
            print(f"{address} not sending data... closing connection and finding a new connection \n")
            connection = False
        else:
            connection = True
            if data.decode('UTF-8') == "test":
                data = ""
                continue
            else:
                print(f"{address}: ", data.decode('UTF-8'))