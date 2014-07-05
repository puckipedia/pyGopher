class DefaultConfig(object):
	data = {}
	def get(self, path, getter):
		self.data[path] = getter

__all__ = ["entries", "getters"]
