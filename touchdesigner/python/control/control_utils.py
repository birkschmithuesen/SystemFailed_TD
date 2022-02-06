from TDStoreTools import StorageManager
import TDFunctions as TDF

class Utils:
	"""
	Control Utils description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.pars = ownerComp.par
		self.Loaded = ownerComp.op('./loaded_cue')
		self.Sceneloader = op.Scene

	def Pause(self):
		self.pars.Timestop.val = 1

	def Unpause(self):
		self.pars.Timestop.val = 0

	def Go(self):
		op.Scene.Load()
		op.Scene.Go()
		self.GoScene()
		self.GoGraphics()
		self.GoSound()

	def GoTo(self, cueIndex):
		sop = op.Scene
		target = tdu.clamp(int(cueIndex), 1, (sop.par.Size.eval() - 1))
		sop.par.Index.val = target
		self.Go()

	def Arm(self):
		self.Sceneloader.par.Index.val = int(self.pars.Preloadindex.eval())

	def GoRelative(self, step):
		sop = op.Scene.par
		curi = sop.Index.eval()
		nexti = tdu.clamp((curi + step), 1, (sop.Size - 1))
		sop.Index = nexti
		self.Go()

	def GoNext(self):
		target = int(self.pars.Followindex.eval())
		self.GoTo(target)

	def GoBack(self):
		target = int(self.pars.Previousindex.eval())
		self.GoTo(target)

	def EndSkip(self, delay = 15):
		# self.Pause()
		# run('op.Control.par.Endround.pulse()', delayFrames = 30*delay)
		# run('op.Control.Unpause()', delayFrames = 30*delay)
		pass

	def GoTable(self, ref):
		table = op(ref)
		for i in range(1, table.numRows):
			name = table[i,'parameter']
			value = table[i,'value']
			path = table[i,'path']
			op(path).par[name] = value
			pass

	def GoScene(self):
		for fop in ops('scene_*'):
			self.GoTable(fop)

	def GoGraphics(self):
		rendercue = self.Loaded[1,'rendering'].val
		colorcue = self.Loaded[1,'colorset'].val
		# debug(rendercue)
		op.Rendercl.Recall_Cue(rendercue)
		#op.Colorcl.Recall_Cue(colorcue)

	def GoSound(self):
		scene = self.Loaded[1,'scene']
		soundIntro =  str(self.Loaded[1,'soundintro'].val)
		soundEval = str(self.Loaded[1,'soundeval'].val)
		soundRound = str(self.Loaded[1,'soundround'].val)
		soundSynth = int(self.Loaded[1,'soundsynth'].val or 0)
		soundTrack = (self.Loaded[1,'soundtrack'].val or 0)
		op.Sound.SendScene(scene)
		op.Sound.SendSynthtoggle(soundSynth)
		if soundTrack == 0:
			op.Sound.SendSoundtrack()
		else:
			soundTrack = str(soundTrack).split(' ')			
			op.Sound.SendSoundtrack(subtype = soundTrack[0], trigger = soundTrack[1])
		if not soundIntro == '':
			op.Sound.SendIntro(soundIntro)
		if not soundEval == '':
			op.Sound.SendEvaluationStart()
		if not soundRound == '':
			op.Sound.SendRound(soundRound)
		