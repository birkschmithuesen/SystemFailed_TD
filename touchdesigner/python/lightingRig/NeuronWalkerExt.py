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

	options = {
		(0,1,2,3,4,5,6,7): (8,9,10,11,12,13,14,15),
		(8,9,10,11,12,13,14,15): (0,1,2,3,4,5,6,7)
	}

	def __init__(self, owner, lampId, options = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)):
		super().__init__()
		self.owner = owner
		if lampId >= 0:
			self.lampManager.RequestLampById(self, lampId)
		else:
			self.lampManager.RequestLamps(self, 1, mode='random', options = options)
		self.nextStep = None
		self.valueFader = None
		self.runObjects = []
		self.options = ()
		for i in NeuronStep.options:
			if self[0].lampId in i:
				self.options = NeuronStep.options[i]

	def __repr__(self):
		return f"NeuronStep#{self.cntId}"

	def append(self, lamp):
		super().append(lamp)
		self.setLampAttributes(lamp)

	def setLampAttributes(self, lamp):
		lamp.activationId = 1
		lamp.height = -1	# to NOT use height in the trackerPosition
		lamp.red = 1
		lamp.green = 1
		lamp.blue = 1
		lamp.white = 1
		lamp.beamSize = 0
		lamp.shutter = 61
		
	def trigger(self):
		#debug('trigger',self, f'{me.time.seconds:.2f}')
		if len(self) == 0:
			debug('i am empty - cannot step!')
			return

		self.nextStep = NeuronStep(self.owner, -1, options = self.options)
		# TODO: call/copy ValueFader, übergibt sich selbst
		# mit positionCallback = nextStep.trigger()
		self.valueFader = op(op.neuronWalker.copy(op('value_fader'), name='val_fd1'))
		self.valueFader.Lamp = self[0]
		self.setupStep()

	def cleanUp(self):
		#debug('cleanUp', self, f'{me.time.seconds:.2f}')
		self.cleanUpRunObjects()
		try:
			self.valueFader.destroy()
		except:
			pass
		self.releaseAllLamps()
		self.owner.append(self.nextStep)
		self.owner.remove(self)


	def delete(self):
		super().delete()
		self.cleanUp()
		if self.nextStep:
			self.nextStep.delete()


	def setupStep(self):
		fader = self.valueFader

		speed = self.owner.speed
		stepFrequency = 0.1 + speed/255 * 9.9
		stepDuration = 1000 / stepFrequency		# in ms
		
		posDelay = max(self.owner.posDelay/255 * stepDuration, 20)	# in ms   # we need some time at least - otherwise, the filter will not work
		posFade = stepDuration - posDelay	# in ms

		fadeInDelay = self.owner.intDelay/255 * stepDuration
		fadeInTime = self.owner.intFadeIn/255 * stepDuration
		intStayTime = self.owner.intStay/127 * stepDuration
		fadeOutDelay = fadeInDelay + fadeInTime + intStayTime
		fadeOutTime = self.owner.intFadeOut/64 * stepDuration
		completeDuration = max(fadeOutDelay + fadeOutTime, stepDuration + 20)

		priorityDelay = self.owner.priorityDelay/64 * stepDuration

		#debug(f'setting up {self} with duration={stepDuration:.0f}, pos={posDelay:.0f}/{posFade:.0f}, int={fadeInDelay:.0f},{fadeInTime:.0f},{intStayTime:.0f},{fadeOutTime:.0f}, prioDel={priorityDelay:.0f}, next={self.nextStep}')
		
		self.valueFader.SetPositionWithoutFadeTime(self[0].trackerPosition)
		self.runObjects.append(run(f'args[0].SetPositionWithFadeTime({self.nextStep[0].position}, {posFade})', self.valueFader, delayMilliSeconds = posDelay))

		self.runObjects.append(run(f'args[0].nextStep.trigger()', self, delayMilliSeconds = stepDuration))

		self.valueFader.SetIntensityWithoutFadeTime(0)
		self.runObjects.append(run(f'args[0].SetIntensityWithFadeTime({self.owner.intensity}, {fadeInTime})', self.valueFader, delayMilliSeconds = fadeInDelay))
		self.runObjects.append(run(f'args[0].SetIntensityWithFadeTime(0, {fadeOutTime})', self.valueFader, delayMilliSeconds = fadeOutDelay))
		self.runObjects.append(run(f'args[0].priority = 0', self, delayMilliSeconds = priorityDelay))
		self.runObjects.append(run(f'args[0].cleanUp()', self, delayMilliSeconds = completeDuration))

	def cleanUpRunObjects(self):
		for run in self.runObjects:
			try:
				run.kill()
			except:
				pass

class NeuronWalkerExt(list):
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
		self.posDelay = 0
		self.shutterStay = 0
		self.startChannel = 301
		self.priorityDelay = 64
		self.dmxManager.subscribeChannel(self.startChannel, {'object': self, 'name':'intensity'})
		self.dmxManager.subscribeChannel(self.startChannel + 1, {'object': self, 'name':'shutter'})
		self.dmxManager.subscribeChannel(self.startChannel + 2, {'object': self, 'name':'speed'})
		self.dmxManager.subscribeChannel(self.startChannel + 3, {'object': self, 'name':'intDelay'})
		self.dmxManager.subscribeChannel(self.startChannel + 4, {'object': self, 'name':'intFadeIn'})
		self.dmxManager.subscribeChannel(self.startChannel + 5, {'object': self, 'name':'intStay'})
		self.dmxManager.subscribeChannel(self.startChannel + 6, {'object': self, 'name':'intFadeOut'})
		self.dmxManager.subscribeChannel(self.startChannel + 7, {'object': self, 'name':'posDelay'})
		self.dmxManager.subscribeChannel(self.startChannel + 8, {'object': self, 'name':'shutterStay'})
		self.dmxManager.subscribeChannel(self.startChannel + 9, {'object': self, 'name':'priorityDelay'})

	@property
	def intensity(self):
		return self._intensity

	@intensity.setter
	def intensity(self, value):
		if hasattr(self, '_intensity'):
			prev = self.intensity
		else:
			prev = 0
		if isinstance(value, int):
			value = value/255
		self._intensity = value
		# TODO: if prev == 0 start new step
		if prev == 0 and value > 0:
			self.newNeuronWalk(-1)
		if value == 0:
			self.StopAllWalks()

	def newNeuronWalk(self, lampId):
		step = NeuronStep(self, lampId)
		step.trigger()
		self.append(step)

	def StopAllWalks(self):
		debug(self)
		for walk in self:
			if walk: walk.delete()
		debug(self)
		# return
		# 	try:
		# 		walk.delete()
		# 	except:
		# 		debug("failed delete")
		# 		pass
