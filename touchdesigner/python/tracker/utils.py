from TDStoreTools import StorageManager, DependList, DependDict

import TDFunctions as TDF

class Utils:
	"""
	Utility Class for the SystemFailed Tracker Container
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.ready = 0
		run("op.Tracker.InitRound()", delayFrames = 300)

	def getTrack(self, trackid):
		try:
			tid = int(trackid)
			track = op('./track_{trackid}')
			return track
		except:
			debug(f'{me}: could not get track for trackid: {trackid}')
			return None

	def tracks(self, ref = 'raw'):
		id_dat = self.ownerComp.op(f'{str(ref)}_id_dat')
		refs = ['track_' + cell.val for cell in id_dat.row(0)]
		# debug(refs)
		refs.insert(0,' ')
		refs.append(' ')
		tracks = ops(refs)
		# debug(tracks)
		return tracks

	def PassPulse(self, parname, trackid = -1):
		# delay = 1
		if not (trackid == -1):
			tracks = [self.getTrack(trackid)]
		else:
			tracks = self.tracks()
		for track in tracks:
			track.par[str(parname)].pulse()

	def SetVal(self, parname, value, trackid = -1):
		# debug(f'SetVal: {parname}, {value}')
		if not (trackid == -1):
			tracks = [self.getTrack(trackid)]
		else:
			tracks = self.tracks()
		for track in tracks:
			track.par[str(parname)].val = value

	def InitRound(self):
		op('group_profile').par.Resetrecord.pulse()
		self.PassPulse('Unfreezesilent')
		self.PassPulse('Unstrike')
		self.PassPulse('Resetscore')
		self.PassPulse('Resetrecord')
		self.SetVal('Timestop', 1)
		self.ready = 1

	def StartRound(self):
		op('group_profile').par.Resetrecord.pulse()
		op('group_profile').par.Startrecord.pulse()
		if not self.ready:
			self.InitRound()
		self.PassPulse('Startrecord')
		self.SetVal('Timestop', 0)
		self.ready = 0
		pass

	def PauseRound(self):
		self.SetVal('Timestop', 1)
		pass

	def ResumeRound(self):
		self.SetVal('Timestop', 0)
		pass

	def StopRound(self):
		op('group_profile').par.Stoprecord.pulse()
		op('group_profile').par.Updatetrail.pulse()
		self.SetVal('Timestop', 1)
		self.PassPulse('Capturehighscore')
		self.PassPulse('Stoprecord')
		self.PassPulse('Updatetrail')
		self.PassPulse('Unfreezesilent')
		# self.PassPulse('Unstrike')