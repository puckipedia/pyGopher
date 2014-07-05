import socket
import sys
from config import GopherConfig

config = GopherConfig()

for i, getter in config.data.items():
	getter.set_default(config.host, config.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.bind(("", int(config.port)))
except socket.error as msg:
	print("Error: ")
	print(msg)
	sys.exit(1)
except ValueError as e:
	print("Port isn't numeric!")
	sys.exit(1)

sock.listen(10)

def one_sock(conn, addr):
	try:
		socket_file = conn.makefile()
		command_line = socket_file.readline()[:-1].split("\t")

		if command_line[0] == "":
			command_line[0] = config.default

		if command_line[0] not in config.data:
			config.not_found(conn, command_line)
		else:
			config.data[command_line[0]].output_data(conn, command_line[1:])
	except BaseException as ex:
		config.on_exception(conn, ex)
	finally:
		conn.shutdown(socket.SHUT_RDWR)
		conn.close()

while True:
	conn, addr = sock.accept()
	one_sock(conn, addr)
