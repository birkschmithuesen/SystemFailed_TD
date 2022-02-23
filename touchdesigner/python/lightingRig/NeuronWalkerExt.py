"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki

1 speed > 0 -> request one Lamp A
2 fade in A
3 request any one Lamp B
4 move Lamp A to B in 'speed' seconds
	- 
5 feed-animation
6 fade out A / fade in B (2)
7 and so on

"""

from lampUser import LampUser

class NeuronStep(LampUser):
	def __init__(self, owner, lampId):
		self.owner = owner
		if lampId >= 0:
			self.lampManager.RequestLampById(self, lampId)
		else:
			self.lampManager.RequestLamps(self, 1)
		self.nextStep = None
		
	def trigger(self):
		if len(self) == 0:
			debug('i am empty - cannot step!')
			return
		self.nextStep = NeuronStep(self.owner, -1)





class NeuronWalkerExt():
	"""
	NeuronWalkerExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.dmxManager = op.DMX.ext.DMXManagerExt
		self.intensity = 0
		self.shutter = 0
		self.speed = 127
		self.intDelay = 0
		self.intFadeIn = 0
		self.intStay = 127
		self.intFadeOut = 127
		self.posWait = 0
		self.shutterStay = 0
		self.startChannel = 301
		self.dmxManager.subscribeChannel(self.startChannel, {'object': self, 'name':'intensity'})
		self.dmxManager.subscribeChannel(self.startChannel + 1, {'object': self, 'name':'shutter'})
		self.dmxManager.subscribeChannel(self.startChannel + 2, {'object': self, 'name':'speed'})
		self.dmxManager.subscribeChannel(self.startChannel + 3, {'object': self, 'name':'intDelay'})
		self.dmxManager.subscribeChannel(self.startChannel + 4, {'object': self, 'name':'intFadeIn'})
		self.dmxManager.subscribeChannel(self.startChannel + 5, {'object': self, 'name':'intStay'})
		self.dmxManager.subscribeChannel(self.startChannel + 6, {'object': self, 'name':'intFadeOut'})
		self.dmxManager.subscribeChannel(self.startChannel + 7, {'object': self, 'name':'posWait'})
		self.dmxManager.subscribeChannel(self.startChannel + 8, {'object': self, 'name':'shutterStay'})

	@property
	def intensity(self):
		return self._intensity

	@intensity.setter
	def intensity(self, value):
		if isinstance(value, int):
			value = value/255
		self._intensity = value
		
	@property
	def shutter(self):
		return self._shutter

	@shutter.setter
	def shutter(self, value):
		if isinstance(value, int):
			value = value/255
		self._shutter = value
		
	@property
	def speed(self):
		return self._speed

	@speed.setter
	def speed(self, value):
		if isinstance(value, int):
			value = value/255
		self._speed = value
		
	@property
	def intDelay(self):
		return self._intDelay

	@intDelay.setter
	def intDelay(self, value):
		if isinstance(value, int):
			value = value/255
		self._intDelay = value
		
	@property
	def intFadeIn(self):
		return self._intFadeIn

	@intFadeIn.setter
	def intFadeIn(self, value):
		if isinstance(value, int):
			value = value/255
		self._intFadeIn = value

	@property
	def intStay(self):
		return self._intStay

	@intStay.setter
	def intStay(self, value):
		if isinstance(value, int):
			value = value/255
		self._intStay = value
		
	@property
	def intFadeOut(self):
		return self._intFadeOut

	@intFadeOut.setter
	def intFadeOut(self, value):
		if isinstance(value, int):
			value = value/255
		self._intFadeOut = value
		
	@property
	def posWait(self):
		return self._posWait

	@posWait.setter
	def posWait(self, value):
		if isinstance(value, int):
			value = value/255
		self._posWait = value
		
	@property
	def shutterStay(self):
		return self._shutterStay

	@shutterStay.setter
	def shutterStay(self, value):
		if isinstance(value, int):
			value = value/255
		self._shutterStay = value
		
	#########################################


