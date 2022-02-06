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

	def Pause(self):
		self.pars.Timestop.val = 1

	def Unpause(self):
		self.pars.Timestop.val = 0

	def Go(self):
		self.GoScene()
		self.GoGraphics()
		self.GoSound()

	def GoRelative(self, step):
		sop = op.Scene.par
		curi = sop.Index.eval()
		nexti = tdu.clamp((curi + step), 0, (sop.Size - 1))
		sop.Index = nexti
		op.Scene.Load()
		op.Scene.Go()
		self.Go()

	def GoNext(self):
		self.GoRelative(1)

	def GoBack(self):
		self.GoRelative(-1)

	def EndSkip(self, delay = 15):
		self.Pause()
		run('op.Control.par.Endround.pulse()', delayFrames = 30*delay)
		run('op.Control.Unpause()', delayFrames = 30*delay)

	def GoTable(self, ref):
		table = op(ref)
		for i in range(1, table.numRows):
			name = table[i,'parameter']
			value = table[i,'value']
			path = table[i,'path']
			op(path).par[name] = value
			pass

	def GoScene(self):
		op.Scene.Go()
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
		soundIntro = self.Loaded[1,'soundintro'].val
		soundEval = self.Loaded[1,'soundeval'].val
		soundRound = self.Loaded[1,'soundround'].val
		op.Sound.SendScene(scene)
		if soundIntro:
			op.Sound.SendIntro(soundIntro)
		if soundEval:
			op.Sound.SendEvaluationStart()
		if soundRound:
			op.Sound.SendRound(soundRound)