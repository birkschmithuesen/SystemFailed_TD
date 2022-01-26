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
		for rowi in range(1, table.rows()):
			pass