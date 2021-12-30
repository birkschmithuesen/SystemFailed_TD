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
		self.PageDict = dict([(e.name, e) for e in ownerComp.customPages])

	def ActivatePage(self, pagename):
		page = self.PageDict[pagename]
		for p in page.pars:
			p.enable = True

	def DeactivatePage(self, pagename):
		page = self.PageDict[pagename]
		for p in page.pars:
			p.enable = False

	def Flagupdate(self):
		active = bool(self.ownerComp.par.Active)
		performer = bool(self.ownerComp.par.Performer)
		jail = bool(self.ownerComp.par.Jail)
		if not active:
			self.SetInactive()
		elif performer:
			self.SetPerformer()
		elif jail:
			self.SetJail()
		else:
			self.SetParticipant()

	def SetInactive(self):
		slot = self.ownerComp
		# slot.name = slot.par.Name
		# slot.par.Active = False
		for pagename in ['Position','Geometry','Score','Poll','Jail','Highlight','Scene']:
			self.DeactivatePage(pagename)
		pass

	def SetPerformer(self):
		slot = self.ownerComp
		# slot.name = slot.par.Name
		# slot.par.Active = False
		for pagename in ['Geometry','Score','Poll','Jail','Highlight','Scene']:
			self.DeactivatePage(pagename)
		for pagename in ['Position']:
			self.ActivatePage(pagename)
		pass

	def SetJail(self):
		slot = self.ownerComp
		# slot.name = slot.par.Name
		# slot.par.Active = False
		for pagename in ['Geometry','Score','Poll']:
			self.DeactivatePage(pagename)
		for pagename in ['Position','Jail','Highlight','Scene']:
			self.ActivatePage(pagename)
		pass

	def SetParticipant(self):
		debug(f'setting {self.ownerComp.par.Trackid} as participant')
		slot = self.ownerComp
		# slot.name = slot.par.Name
		# slot.par.Active = False
		for pagename in ['Basic', 'Position', 'Geometry', 'Score', 'Poll', 'Jail', 'Highlight', 'Scene']:
			self.ActivatePage(pagename)
		pass

	def SetGeoGrab(self):
		pass

	def UnsetGeoGrab(self):
		pass

	def Reset(self):
		pass

	def RoundReset(self):
		pass

	def RoundStore(self):
		pass

	def RoundRemove(self):
		pass
