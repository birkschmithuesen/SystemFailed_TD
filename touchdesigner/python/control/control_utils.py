from TDStoreTools import StorageManager
import TDFunctions as TDF

class Utils:
	"""
	Control Utils description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

	def GoTable(self, ref):
		table = op(ref)
		for i in range(1, table.numRows):
			name = table[i,'name']
			value = table[i,'value']
			path = table[i,'path']
			op(path).par[name].val = value
			pass

	def Black(self):
		self.GoTable('graphics_black')

	def Defaults(self):
		self.GoTable('graphics_platformdefault')

