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
	Utils description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		osc1 = op('sender')
		osc2 = op('sender_debug')
		self.oscSenders = [osc1, osc2]

	def Send(self, message, args):
		for s in self.oscSenders:
			debug(f'{self.ownerComp} sending osc on {s}:\n {message}, {args}')
			s.sendOSC(message, args, asBundle=False, useNonStandardTypes=True)
	