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
		tracks = ops(refs)
		return tracks

	def PassPulse(self, parname, trackid = -1):
		if not (trackid == -1):
			tracks = [self.getTrack(trackid)]
		else:
			tracks = self.tracks()
		for track in tracks:
			track.par[str(parname)].pulse()

	def SetVal(self, parname, value, trackid = -1):
		if not (trackid == -1):
			tracks = [self.getTrack(trackid)]
		else:
			tracks = self.tracks()
		for track in tracks:
			track.par[str(parname)].val = value


	def StartRound(self):
		#RESET STATE
		PassPulse('Unfreeze')
		PassPulse('Unstrike')
		PassPulse('Unstrike')
		PassPulse('Resetscore')
		PassPulse('Resetrecord')
		PassPulse('Startrecord')
		pass

	def StopRound(self):
		PassPulse('Capurehighscore')
		PassPulse('Stoprecord')