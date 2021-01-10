import socket


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 5555


	def connect(self, ip):
		self.server = ip
		self.addr = (self.server, self.port)
		try:
			self.client.connect(self.addr)
			print("connected to: " + str(self.addr))
			return True
		except ConnectionRefusedError:
			print("error: connection refused.")
			return False
		except OSError:
			print("error: invalid IP.")
			


	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()
		except socket.error as e:
			print(e)

