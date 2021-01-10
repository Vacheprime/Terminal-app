import socket
import pickle
import rsa
from _thread import *

(P_k, Pr_k) = rsa.newkeys(1024)

server = socket.gethostbyname(socket.gethostname())
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
print("IP of this server " + str(socket.gethostbyname(socket.gethostname())))
print("To connect: give the ip of the server to clients")


def threaded(conn, addr):
	global connections
	global P_k
	global Pr_k
	reply = ""
	CP_k = pickle.loads(conn.recv(2048))
	CL = Client(CP_k, conn)
	connections.append(CL)
	CL.ip.send(pickle.dumps(P_k))
	quitmsg = pickle.loads(rsa.decrypt(conn.recv(2048), Pr_k))
	while True:
		try:
			data1 = conn.recv(2048)
			data2 = rsa.decrypt(data1, Pr_k)
			reply = pickle.loads(data2)
			split = reply.split(":")
			if not data1:
				break
			elif split[1] == quitmsg:
				break
			else:
				pass
			for i, cl in enumerate(connections):
				try:
					cl.ip.sendall(rsa.encrypt(pickle.dumps(reply), cl.k))
				except:
					print("error")
		except:
			break
	connections.remove(CL)
	conn.close()
	print("lost connection to" + str(addr))
	

while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    start_new_thread(threaded, (conn, addr))

