from Functions import Function
from tNetwork import Network
import subprocess, rsa, pickle
from _thread import *

is_connected = False
quitword = ""
chatapp_cmd = ["connect"]
cmd = ""
location = "home"


def scan(PR_k, ):
	global quitword
	while True:
		try:
			msg = pickle.loads(rsa.decrypt(n.client.recv(2048), PR_k))
			print(msg)
		except:
			break
		
def post(SP_k):
	global is_connected
	global quitword
	username = input("enter username:")
	quitword = input("enter quit word:")
	n.client.sendall(rsa.encrypt(pickle.dumps(quitword), SP_k))
	while True:
		msg = input()
		try:
			n.client.sendall(rsa.encrypt(pickle.dumps(username + ":" + msg), SP_k))
			if msg == quitword:
				is_connected = False
				print("disconnected.")
				break
		except:
			print("an error ocurred sending a message.")
			break
		
while cmd != "exit":
	#  input and arguments
	cmd = str(input(location + ">> "))
	args = cmd.split()
	# clear command
	if cmd == "clear":
		subprocess.run("clear")
	# cd command
	elif len(args) > 0 and args[0] == "cd":
		cd = Function.cd(args, location)
		location = cd
	# chatapp commands
	elif location == "chatapp" and len(args) > 0 and args[0] in chatapp_cmd:
		if args[0] == "connect":
			if len(args) == 2:
				n = Network()
				is_connected = n.connect(args[1])
				if is_connected == True:
					(P_k, PR_k) = rsa.newkeys(1024)
					n.client.send(pickle.dumps(P_k))
					SP_k = pickle.loads(n.client.recv(2048))
					
					start_new_thread(scan, (PR_k, ))
					post(SP_k)
			else:
				if len(args) < 2:
					print("error: no IP specified.")
				elif len(args) > 2:
					print("error: unexpected argument.")
					
	elif len(args) > 0 and cmd != "exit":
		print("error: unknown command.")
