import socket
import sys
import threading
import imp
import signal

import config

server_config = config.GopherConfig()

for i, getter in server_config.data.items():
	getter.set_default(server_config.host, server_config.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.bind(("", int(server_config.port)))
except socket.error as msg:
	print("Error: ")
	print(msg)
	sys.exit(1)
except ValueError as e:
	print("Port isn't numeric!")
	sys.exit(1)

sock.listen(10)

def reload_config(a, b):
	imp.reload(config)
	server_config = config.GopherConfig()
	for i, getter in server_config.data.items():
		getter.set_default(server_config.host, server_config.port)
	print("Reloaded config! I haven't set the new host+port, however")

signal.signal(signal.SIGUSR1, reload_config)

class GopherConnection(threading.Thread):
	def __init__(self, connect, ip, port):
		threading.Thread.__init__(self)
		self.conn = connect
		self.ip = ip
		self.port = port
		print("[+] Got connection!")
	def run(self):
		try:
			socket_file = self.conn.makefile()
			command_line = socket_file.readline()[:-1].split("\t")

			print(command_line[0])
			if command_line[0][-8:] == "HTTP/1.1":
				path = command_line[0].split(" ")[1]
				if path not in server_config.data:
					server_config.not_found(self.conn, command_line)
				else:
					server_config.data[path].output_data(self.conn, command_line[1:])
			else:
				if command_line[0] == "":
					command_line[0] = server_config.default

				if command_line[0] not in server_config.data:
					server_config.not_found(self.conn, command_line)
				else:
					server_config.data[command_line[0]].output_data(self.conn, command_line[1:])
		except OSError as ex:
			pass
		except BaseException as ex:
			server_config.on_exception(self.conn, ex)
		finally:
			self.conn.shutdown(socket.SHUT_RDWR)
			self.conn.close()

while True:
	try:
		(conn, (ip, port)) = sock.accept()
		GopherConnection(conn, ip, port).start()
	except InterruptedError as e:
		pass
