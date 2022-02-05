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

class Utils:
	"""
	Utils description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.pars = ownerComp.par
		self.Grabs = ownerComp.ops('*readlive')
		self.Writes = ownerComp.ops('*writelive')
		self.Files = ownerComp.ops('*file')

	def WriteSnapshot(self, components = []):
		if len(components):
			for comp in components:
				fop = op(f'{comp}_writelive')
				fop.par.write.pulse()
				# fop.save(fop.par.file.val, createFolders=True)
		else:
			for fop in self.Writes:
				# fop.save(fop.par.file.val, createFolders=True)
				fop.par.write.pulse()

	def Write(self, components = []):
		folder = self.pars.Livefolder.eval()
		mod.os.makedirs(f'{project.folder}/{folder}', exist_ok=True)
		if len(components):
			for comp in components:
				fop = op(f'{comp}_file')
				# fop.save(fop.par.file.val, createFolders=True)
				fop.par.writepulse.pulse()
		else:
			for fop in self.Files:
				fop.par.writepulse.pulse()
				# fop.save(fop.par.file.val, createFolders=True)

	def Load(self, components = []):
		if len(components):
			for comp in components:
				op(f'{comp}_file').par.loadonstartpulse.pulse()
		else:
			for fop in self.Files:
				fop.par.loadonstartpulse.pulse()

	def Go(self, components = []):
		if len(components):
			for comp in components:
				op(comp).copy(f'{comp}_file')
		for fop in self.Files:
			# e.g. 'guide_file' -> 'guide'
			go = self.ownerComp.op(fop.name.split('_')[0])
			op(go).copy(fop)

	def GoToTable(self, handle):
		table = op(handle)
		return