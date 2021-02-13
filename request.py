import socket, pickle
import rsa

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 5555
		self.Public_key = None
		self.Private_key = None


	def define_keys(self):
		if self.Public_key == None and self.Private_key == None:
			print("Generating keys...")
			(self.Public_key, self.Private_key) = rsa.newkeys(1024)
			print("Finished.")
		else:
			print("Keys already defined. Skipping step.")


	def connect(self, ip):
		self.server = ip
		self.addr = (self.server, self.port)
		try:
			self.client.connect(self.addr)
			print("connected to: " + str(self.addr))
			return True
		except ConnectionRefusedError:
			print(f"error: connection refused. Tried to connect using: {ip}")
			return False
		except OSError:
			print("error: invalid IP.")



	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()
		except socket.error as e:
			print(e)


	def download(self, args):
		print("Sending public key...")
		self.client.send(pickle.dumps(self.Public_key))
		print("Receiving server public key...")
		Server_pk = pickle.loads(self.client.recv(2048))
		file = str(args[2] + ".py")

		fullmessage = [str(args[1]), str(file)]
		print(f"Sending: {fullmessage}")
		self.client.send(rsa.encrypt(pickle.dumps(fullmessage), Server_pk))

		size = pickle.loads(rsa.decrypt(self.client.recv(2048), self.Private_key))
		print(f"File length: {size}")
		size = int(size)
		tool = pickle.loads(rsa.decrypt(self.client.recv(2048), self.Private_key))
		with open(f"{file}", "w") as f:
			f.write(tool)
			f.close()
		print(f"Finished download. To add to path do: chtool add {args[2]}")



def run(args, cmd):
	if args[1] == "download":
		n = Network()
		with open("repo_info.txt", "rb") as f:
			repo_ip = str(pickle.load(f))
			f.close()
		if len(repo_ip) == 0:
			print("No repository selected.")
		elif len(repo_ip) != 0:
			status = n.connect(repo_ip)
			if status == True:
				n.define_keys()
				n.download(args)
	elif args[1] == "addrepo":
		with open("repo_info.txt", "wb") as f:
			pickle.dump(args[2], f)
			f.close()
			print(f"Added {args[2]} to repository.")
	elif args[1] == "info":
		with open("repo_info.txt", "rb") as f:
			print(f"Target: {pickle.load(f)}")
			f.close()
	else:
		print("Invalid arguments.")
