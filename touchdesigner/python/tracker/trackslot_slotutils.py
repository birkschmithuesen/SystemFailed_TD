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

class Slotutils:
	"""
	Slotutils description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Flagupdate(self):
		active = bool(self.ownerComp.par.Active.eval())
		performer = bool(self.ownerComp.par.Performer.eval())
		freeze = bool(self.ownerComp.par.Freeze.eval())
		if not active:
			self.SetInactive()
		elif performer:
			self.SetPerformer()
		elif freeze:
			self.SetFreeze()
		else:
			self.SetParticipant()

	def SetInactive(self):
		self.ownerComp.Reset()
		self.ownerComp.par.Timestamp.val = 0
		pass

	def SetPerformer(self):
		slot = self.ownerComp
		pass

	def SetJail(self):
		pass

	def SetParticipant(self):
		pass

	def Reset(self):
		pass

	def Resetscore(self):
		pass

	def Resetrecord(self):
		pass

	def Startrecord(self):
		pass

	def Stoprecord(self):
		pass

	def SetFreeze(self):
		op('./freeze').par.Forcefreeze.pulse()
		pass
	
	def Unfreeze(self):
		op('./freeze').par.Unfreeze.pulse()
		pass	