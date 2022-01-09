from TDStoreTools import StorageManager, DependList, DependDict

import TDFunctions as TDF

class Utils:
	"""
	Utility Class for the SystemFailed Tracker Container
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def getTrack(self, trackid):
		try:
			tid = int(trackid)
			track = op('./track_{trackid}')
			return track
		except:
			debug(f'{me}: could not get track for trackid: {trackid}')
			return None

	def Unstrike(self, trackid):
		track = self.getTrack(trackid)
		track.par.Unstrike.pulse()

	def UnstrikeAll(self):
		for tid in range(1,51):
			self.Unstrike(tid)

	def Unfreeze(self, trackid):
		track = self.getTrack(trackid)
		track.par.Unfreeze.pulse()

	def UnfreezeAll(self):
		for tid in range(1,51):
			self.Unfreeze(tid)

	def ResetRoundtotal(self, trackid):
		track = self.getTrack(trackid)
		track.par.Resetroundtotal.pulse()

	def ResetRoundtotalAll(self):
		for tid in range(1,51):
			self.ResetRoundtotal(tid)

	def CaptureHighscore(self, trackid):
		pass

	def CaptureHighscoreAll(self):
		pass

	def StartRoundrecord(self):
		pass

	def StopRoundrecord(self):
		pass

	def ResetRoundrecord(self):
		pass