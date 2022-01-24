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

	def tracks(self, ref = 'raw'):
		id_dat = self.ownerComp.op(f'{str(ref)}_id_dat')
		refs = ['track_' + cell.val for cell in id_dat.row(0)]
		# debug(refs)
		refs.insert(0,'')
		refs.append('')
		tracks = ops(refs)
		# debug(tracks)
		return tracks

	def PassPulse(self, parname, trackid = -1):
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


	def StartRound(self):
		#RESET STATE
		self.PassPulse('Unfreeze')
		self.PassPulse('Unstrike')
		self.PassPulse('Unstrike')
		self.PassPulse('Resetscore')
		self.PassPulse('Resetrecord')
		self.PassPulse('Startrecord')
		self.SetVal('Timestop', 0)
		pass

	def PauseRound(self):
		self.SetVal('Timestop', 1)
		pass

	def ResumeRound(self):
		self.SetVal('Timestop', 0)
		pass

	def StopRound(self):
		self.SetVal('Timestop', 1)
		self.PassPulse('Capturehighscore')
		self.PassPulse('Stoprecord')
		self.PassPulse('Unfreeze')
		self.PassPulse('Unstrike')
	
	def EvaluateRound(self):
		#TRIGGER EVAL CALLOUT TIMER
		pass