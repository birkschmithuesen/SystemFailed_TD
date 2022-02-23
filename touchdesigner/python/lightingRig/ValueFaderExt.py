"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

class ValueFaderExt:
	"""
	PositionFaderExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.positionStartCHOP = op('position')
		self.positionFilterCHOP = op('position_filter')
		self.Position = (0,0,0)
		self.PositionTime = 0

	@property
	def Position(self):
		return self._position

	@Position.setter
	def Position(self, value):
		print("setStart")
		self._position = value
		self.positionFilterCHOP.par.width = 0
		for i in range(3):
			self.positionStartCHOP.par[f'value{i}'] = value[i]

	def startPositionFade(self):
		run(f'args[0].setPositionWithFadeTime({value},10)', self, delayFrames = 3)

	def setPositionWithFadeTime(self, position, fadeTime):
		self.PositionTime = fadeTime
		self.Position = position

	def updateValues(self):
		deltaX = abs(self.Position[0]-self.positionFilterCHOP['x'].eval())
		deltaY = abs(self.Position[1]-self.positionFilterCHOP['y'].eval())
		deltaZ = abs(self.Position[2]-self.positionFilterCHOP['z'].eval())
		if deltaX < 0.000001 and deltaY < 0.000001 and deltaZ < 0.000001:
			# ziel erreicht, callback aufrufen
			print('callback')
