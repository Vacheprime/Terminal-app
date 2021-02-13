import socket
import pickle
import rsa
import os
from _thread import *

(P_k, Pr_k) = rsa.newkeys(1024)
server = input("Server IP: ")
port = 5555
connections = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)


class Client:
	def __init__(self, k, ip):
		self.k = k
		self.ip = ip


s.listen(5)
print("waiting connections")
print(f"IP of this server {server}")
print("To connect: give the ip of the server to clients")


def threaded(conn, addr):
    try:
        global connections
        global P_k
        global Pr_k
        reply = ""
        CP_k = pickle.loads(conn.recv(2048))
        conn.send(pickle.dumps(P_k))
    except:
        print("lost connection to" + str(addr))
        conn.close()
    while True:
        try:
            data1 = conn.recv(2048)
            data2 = rsa.decrypt(data1, Pr_k)
            reply = pickle.loads(data2)
            if not data1:
                break
            else:
                if reply[0] == "download":
                    if os.path.exists(f"tools/{reply[1]}"):
                        with open(f"tools/{reply[1]}", "r") as f:
                            file = f.read()
                            f.close()
                            lenght = len(rsa.encrypt(pickle.dumps(str(file)), CP_k))
                            print(f"Sending length: ({lenght}) info...")
                            conn.sendall(rsa.encrypt(pickle.dumps(str(lenght)), CP_k))
                            print("Sending file...")
                            conn.sendall(rsa.encrypt(pickle.dumps(str(file)), CP_k))
                            print("Done!")
                            break
        except:
            break
    print("lost connection to" + str(addr))
    conn.close()


while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    start_new_thread(threaded, (conn, addr))
