import os
import socket
port = 4040

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", port))
s.listen(1)
connection = False
print("Making a socket was succesful! \n")
def open_log_file():
    global log
    try:
        log = open("logs/log.txt", "w")
    except FileNotFoundError:
        print("Error opening the file")
        if os.path.isdir("logs"):
            log = open("logs/log.txt", "a+")
        else:
            os.mkdir("logs")
            log = open("logs/log.txt", "a+")
    except Exception as e:
        print("Unknown error happened using/opening the file: ", e)

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
                received_data = str(address) + ": " + data.decode('UTF-8')
                print(received_data)
                open_log_file() #Open log file
                log.write(received_data) #Write sent data
                log.close() #Commit changes
                # Hoida tää loppuun ^ Heittää erroria