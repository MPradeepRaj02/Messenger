#BUG in Transmitting a image file was Rectified
#BY MPR

import socket
from threading import Thread
import cv2, socket, numpy, pickle
from time import gmtime, strftime
from random import randint

SERVER = 'localhost'  # localhost
PORT = 1501
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")


server.listen(1)
conn, addr = server.accept()
print(f"[NEW CONNECTION] {conn} : {addr} connected.")


class Send(Thread):
    def run(self):
        while True:
            msg = input("Enter Message to Send\n>>")
            msg = msg.encode()
            conn.send(msg)
            print(f"Msg Sent to {addr}")

class Receive(Thread):
    def run(self):
        while True:
            r_msg = conn.recv(1024)
            r_msg = r_msg.decode()
            print("[RECEIVED MESSAGE] : " + r_msg)

def Stream():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = SERVER 
    port = PORT
    s.bind((ip, port))
    while True:
        x = s.recvfrom(1000000)
        clientip = x[1][0]
        data = x[0]
        print(data)
        data = pickle.loads(data)
        print(type(data))
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('server', data)  # to open image
        if cv2.waitKey(10) == ord('p'):
            break
    cv2.destroyAllWindows()


def ReceivePic():
    imgcounter = 1
    basename = "image%s.png"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()

    while True:
        data = sock.recv(4096)
        txt = str(data)
        print(txt)
        if data:
            if data.startswith('imgsize'):
                tmp = txt.split()
                size = int(tmp[1])
                print('got size')
                sock.sendall("GOT SIZE")

            elif data.startswith('done'):
                sock.shutdown()

            else :
                myfile = open(basename % imgcounter, 'wb')
                myfile.write(data)
                data = sock.recv(40960000)
                if not data:
                    myfile.close()
                    break
                
                myfile.write(data)
                myfile.close()
                sock.sendall("GOT IMAGE")
                sock.shutdown()
                imgcounter += 1


t1 = Send()
t2 = Receive()
t1.start()
t2.start()
ReceivePic()
Stream()