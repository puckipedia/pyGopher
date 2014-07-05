import sys
import gopher
import traceback

from gopher.entries import *
from gopher.getters import *

class ExceptionEntry():
	def set_default(self, a, b):
		pass
	def make_line(self):
		raise Exception("ExceptionEntry called!")

class GopherConfig(gopher.DefaultConfig):
	host = "83.84.127.137"
	port = 7070
	default = "/"

	def __init__(self):
		self.get("/", MenuGetter([
			InfoEntry(" -- This is a test! -- "),
			FileEntry("Hello, World!", "/testhello"),
			DirectoryEntry("99 Bottles Of Beer", "/bottlesofbeer"),
			DirectoryEntry("Another server", "/", host="smar.fi", port="7070"),
			GIFImageEntry("CAT!", "/cat"),
			DirectoryEntry("Throw an Exception", "/exception")]))

		self.get("/bottlesofbeer", MenuGetter([
			FileEntry("99 Bottles Of Beer - Ran!", "/bottlesofbeer/run"),
			FileEntry("99 Bottles Of Beer - Source!", "/bottlesofbeer/code")]))

		self.get("/testhello", TextFileGetter("./www/test.txt"))
		self.get("/bottlesofbeer/run", ExecutableGetter("./www/bacon"))
		self.get("/bottlesofbeer/code", TextFileGetter("./www/bacon"))
		self.get("/cat", BinaryFileGetter("./www/cat.gif"))
		self.get("/exception", ExceptionEntry())

	def not_found(self, socket, data):
		MenuGetter([
			ErrorEntry("Path {} not found!".format(data[0])),
			InfoEntry("Did you spell it correctly?")]).output_data(socket, [])
		print("NOT FOUND")

	def on_exception(self, socket, ex):
		(type, value, trace) = sys.exc_info()
		arr = []
		arr.append(ErrorEntry("The server had an exception!"))
		arr.append(ErrorEntry("Please don't break it!"))
		tb = traceback.format_exception(type, value, trace)
		for i in "\n".join(tb).split("\n"):
			arr.append(InfoEntry(i.replace("\t", "    ")))
		MenuGetter(arr).output_data(socket, [])
