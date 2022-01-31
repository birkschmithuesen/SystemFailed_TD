from TDStoreTools import StorageManager
import TDFunctions as TDF

class Utils:
	"""
	Control Utils description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.pars = ownerComp.par

	def Pause(self):
		self.pars.Timestop.val = 1

	def Unpause(self):
		self.pars.Timestop.val = 0

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
			op(path).par[name].val = value
			pass

	def GoScene(self):
		for fop in ops('scene_*'):
			GoTable(fop)

	def Black(self):
		self.GoTable('graphics_black')

	def Defaults(self):
		self.GoTable('graphics_platformdefault')

