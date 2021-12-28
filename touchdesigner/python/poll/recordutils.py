"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

class Utils:
	"""
	Utils for SystemFailed Poll/Record Component
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.recordDat = ownerComp.op('./data')

	def Write(self, answerlist):
		rd = self.recordDat
		rd.clear()
		rd.appendRow(['Trackid', 'Answer'])
		for ans in answerlist:
			tid = ans[0]
			val = ans[1]
			rd.appendRow([tid,val])