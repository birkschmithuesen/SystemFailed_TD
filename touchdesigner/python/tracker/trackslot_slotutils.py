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
		self.pars = ownerComp.par
		self.Freezeop = ownerComp.op('freeze')
		self.Freezeop.par.Init.pulse()
		self.Scoreop = ownerComp.op('score')
		self.Recorderop = ownerComp.op('recorder')
		self.Neighboursop = ownerComp.op('neighbours')

	def Reset(self):
		pass

	def Flagupdate(self):
		active = bool(self.ownerComp.par.Active.eval())
		performer = bool(self.ownerComp.par.Performer.eval())
		freeze = bool(self.ownerComp.par.Freeze.eval())
		if not active:
			self.SetActive(False)
		elif performer:
			self.SetPerformer()
		elif freeze:
			self.SetFreeze()
		else:
			self.SetParticipant()

	def SetActive(self, val=True):
		if val:
			self.ownerComp.Timestamp.val = absTime.seconds
		else:
			self.ownerComp.Logofftime.val = absTime.seconds
			self.ownerComp.Reset()
		pass

	def SetPerformer(self, val=True):
		pass

	def SetParticipant(self, val=True):
		pass

	def Resetscore(self):
		if not self.pars.Benched:
			self.Scoreop.Roundreset()
			return self.pars.Score
		return 0

	def Resetrecord(self):
		pass

	def Startrecord(self):
		pass

	def Stoprecord(self):
		pass

	def SetFreeze(self):
		self.freezeop.Forcefreeze()
		pass
	
	def Unfreeze(self):
		op('./freeze').par.Unfreeze.pulse()
		pass