class Entry(object):
	type = "0"
	name = ""
	selector = ""
	host = ""
	port = ""
	
	def __init__(self, type="0", name="", selector="", host="", port=""):
		if "\t" in name:
			raise ValueError("There is a tab in the name")

		if "\t" in selector:
			raise ValueError("There is a tab in the name")

		if "\t" in host:
			raise ValueError("There is a tab in the name")

		if port != "":
			try:
				int(port)
			except ValueError as e:
				raise ValueError("Port isn't numeric!")

		self.type = type
		self.name = name
		self.selector = selector
		self.host = host
		self.port = port

	def set_default(self, host, port):
		if self.host == "":
			self.host = host
		if self.port == "":
			self.port = port

	def make_line(self):
		return "{}{}\t{}\t{}\t{}\r\n".format(
			self.type, self.name, self.selector, self.host, self.port).encode("UTF-8")

class BinaryFileEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("9", name, selector, host, port)

class BinHexedEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("4", name, selector, host, port)

class DirectoryEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("1", name, selector, host, port)

class DOSBinaryArchiveEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("5", name, selector, host, port)

class ErrorEntry(Entry):
	def __init__(self, name, selector="", host="error.host", port="1"):
		super().__init__("3", name, selector, host, port)

class FileEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("0", name, selector, host, port)

class GIFImageEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("g", name, selector, host, port)

class ImageEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("I", name, selector, host, port)

class IndexSearchEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("7", name, selector, host, port)

class InfoEntry(Entry):
	def __init__(self, name, selector="", host="error.host", port="1"):
		super().__init__("i", name, selector, host, port)

class RedundantServerEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("+", name, selector, host, port)

class TelnetEntry(Entry):
	def __init__(self, name, username, host="", port=""):
		super().__init__("8", name, username, host, port)

class TN3270SessionEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("T", name, selector, host, port)

class UUEncodedFileEntry(Entry):
	def __init__(self, name, selector, host="", port=""):
		super().__init__("6", name, selector, host, port)
