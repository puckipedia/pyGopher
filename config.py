import sys
import gopher
import traceback

from gopher.entries import *
from gopher.getters import *

class GopherConfig(gopher.DefaultConfig):
	host = "localhost"
	port = "7071"
	default = "/"

	def __init__(self):
		self.menu = MenuGetter([
			InfoEntry(" -- This is a test! -- "),
			DirectoryEntry("This is a directory entry", "/test1"),
			FileEntry("Hello, World!", "/testhello")])
		self.get("/", self.menu)
		self.get("/test1", self.menu)
		self.get("/testhello", TextFileGetter("./www/test.txt"))
		self.get("/bacon", ExecutableGetter("./www/bacon"))

	def not_found(self, socket, data):
		MenuGetter([
			ErrorEntry("Path {} not found!".format(data[0])),
			InfoEntry("Did you spell it correctly?")]).output_data(socket, data[1:])

	def on_exception(self, socket, ex):
		(type, value, trace) = sys.exc_info()
		arr = []
		arr.append(ErrorEntry("The server had an exception!"))
		tb = traceback.format_exception(type, value, trace)
		for i in "\n".join(tb).split("\n"):
			arr.append(InfoEntry(i.replace("\t", "    ")))
		MenuGetter(arr).output_data(socket, [])
