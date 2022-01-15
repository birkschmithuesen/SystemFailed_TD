"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager, DependDict, DependList
import TDFunctions as TDF

class Highscores:
	"""
	Functionality for storing & recalling highscores on a per round basis in the SystemFailed tracker/trackslot/score component  
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.Roundscores = DependDict()

	def UpdateRound(self, ident, value):
		# 0 < value < 100
		try:
			prev = int(self.Roundscores.get(ident, 0)) 
		except TypeError:
			prev = -1
		finally:
			if prev < value:
				self.Roundscores[ident] = value
				return True
			else:
				return False

	def Sum(self):
		sum = 0
		for val in self.Roundscores.values():
			sum += val
		return sum

	def Query(self, ident):
		val = self.Roundscores.get(ident)
		return val