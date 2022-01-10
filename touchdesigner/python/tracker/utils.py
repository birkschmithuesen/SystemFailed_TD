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
		track = self.getTrack(trackid)
		track.par.Capturehighscore.pulse()
		pass

	def CaptureHighscoreAll(self):
		for tid in range(1,51):
			self.CaptureHighscore(tid)		
		pass

	def StartRoundrecord(self, trackid):
		track = self.getTrack(trackid)
		track.par.Startroundrecord.pulse()
		pass

	def StartRoundrecordAll(self):
		for tid in range(1,51):
			self.StartRoundrecord(tid)

	def StopRoundrecord(self, trackid):
		track = self.getTrack(trackid)
		track.par.Stoproundrecord.pulse()
		pass

	def StopRoundrecordAll(self):
		for tid in range(1,51):
			self.StopRoundrecord(tid)

	def ResetRoundrecord(self, trackid):
		track = self.getTrack(trackid)
		track.par.Resetroundrecord.pulse()
		pass

	def ResetRoundrecordAll(self):
		for tid in range(1,51):
			self.ResetRoundrecord(tid)
