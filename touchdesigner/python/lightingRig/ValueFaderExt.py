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
	ValueFaderExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.positionCHOP = op('position')
		self.positionFilterCHOP = op('position_filter')
		self.Position = (0,0,0)
		self.intensityCHOP = op('intensity')
		self.intensityFilterCHOP = op('intensity_filter')
		self.Intensity = 0
		self.Lamp = None

	@property
	def Position(self):
		return self._position

	@Position.setter
	def Position(self, value):
		self._position = value
		for i in range(3):
			self.positionCHOP.par[f'value{i}'] = value[i]

	@property
	def Intensity(self):
		return self._intensity

	@Intensity.setter
	def Intensity(self, value):
		self._intensity = value
		for i in range(3):
			self.intensityCHOP.par['value0'] = value

	def SetPositionWithoutFadeTime(self, position):
		self.positionFilterCHOP.par.width = 0
		self.Position = position

	def SetPositionWithFadeTime(self, position, fadeTime):
		self.positionFilterCHOP.par.width = fadeTime/1000
		self.Position = position

	def SetIntensityWithoutFadeTime(self, intensity):
		self.intensityFilterCHOP.par.width = 0
		self.Intensity = intensity

	def SetIntensityWithFadeTime(self, intensity, fadeTime):
		self.intensityFilterCHOP.par.width = fadeTime/1000
		self.Intensity = intensity

	def updateValues(self):
		# set trackerPosition and Intensity in lamp
		x = self.positionFilterCHOP['x'].eval()
		y = self.positionFilterCHOP['y'].eval()
		z = self.positionFilterCHOP['z'].eval()
		intensity = self.intensityFilterCHOP[0].eval()
		if self.Lamp:
			self.Lamp.intensity = intensity
			self.Lamp.trackerPosition = (x,y,z)


		# callback just called after time. This would be to complicated:
		# if callable(self.PositionCallback):
		# 	deltaX = abs(self.Position[0]-self.positionFilterCHOP['x'].eval())
		# 	deltaY = abs(self.Position[1]-self.positionFilterCHOP['y'].eval())
		# 	deltaZ = abs(self.Position[2]-self.positionFilterCHOP['z'].eval())
		# 	if deltaX < 0.000001 and deltaY < 0.000001 and deltaZ < 0.000001:
		# 		# ziel erreicht, callback aufrufen
		# 		print('callback')
		# 		self.PositionCallback = None

