from subprocess import Popen, PIPE

class Getter(object):
	def __init__(self):
		pass
	
	def output_data(self, socket, extra_info):
		socket.sendall("\r\n.\r\n")

	def set_default(self, host, port):
		pass

class MenuGetter(Getter):
	menu_data = []

	def __init__(self, menu):
		self.menu_data = menu

	def set_default(self, host, port):
		for item in self.menu_data:
			item.set_default(host, port)

	def output_data(self, socket, extra_info):
		for item in self.menu_data:
			socket.sendall(item.make_line())
		socket.sendall(".\r\n".encode("utf-8"))

class TextFileGetter(Getter):
	file_path = ""

	def __init__(self, path):
		self.file_path = path

	def output_data(self, socket, extra_info):
		file = open(self.file_path, 'r')
		for line in file:
			if line[0] == ".":
				socket.sendall(("."+line).encode("UTF-8"))
			else:
				socket.sendall(line.encode("UTF-8"))
		socket.sendall("\r\n.\r\n".encode("UTF-8"))

class ExecutableGetter(Getter):
	file_path = ""
	binary = False

	def __init__(self, path, is_binary=False):
		self.file_path = path
		self.binary = is_binary

	def output_data(self, socket, extra_data):
		proc = Popen([self.file_path], stdout=PIPE)
		stdout = proc.stdout

		for line in stdout:
			if line[0] == "." and not self.binary:
				encoded_line = line.decode("UTF-8")
				socket.sendall(("."+encoded_line).encode("UTF-8"))
			else:
				socket.sendall(line)
		if not self.binary:
			socket.sendall("\r\n.\r\n".encode("UTF-8"))
class BinaryFileGetter(Getter):
	file_path = ""

	def __init__(self, path):
		self.file_path = path

	def output_data(self, socket, extra_info):
		file = open(self.file_path, 'rb')
		data = file.read(1024)
		while len(data) > 0:
			socket.sendall(data)
			data = file.read(1024)

