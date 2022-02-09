"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""


class Lamp:
	def __init__(self, lampId):
		self.purpose = None
		self.lampId = lampId
		self.level = 1.0
		self.activationId = None
		self._trackerPosition = {'x':0, 'y':0, 'z':0}
		self.oscSender = parent.Guide.op('./oscout')

	def __repr__(self):
		return f"lamp#{self.lampId} has purpose {self.purpose}"

	@property
	def trackerPosition(self):
		return self._trackerPosition
	
	@trackerPosition.setter
	def trackerPosition(self, value):
		self._trackerPosition = value

	@property
	def color(self):
		return self._colorId

	@color.setter
	def color(self, value):
		self._colorId = value
		oscMessage = f'/exec/14/{value}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)

	@property
	def shutter(self):
		return self._shutterId

	@shutter.setter
	def shutter(self, value):
		self._shutterId = value
		oscMessage = f'/exec/12/{value}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)

	@property
	def beam(self):
		return self._beamId

	@beam.setter
	def beam(self, value):
		self._beamId = value
		oscMessage = f'/exec/12/{value}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)


	def activate(self, activationId):
		self.activationId = int(activationId)
		act_ex = f'/exec/13/{int(activationId) + self.lampId}'
		self.oscSender.sendOSC(act_ex, [self.level], useNonStandardTypes=True)

	def deactivate(self):
		act_ex = f'/exec/13/{self.activationId + self.lampId}'
		self.oscSender.sendOSC(act_ex, [0], useNonStandardTypes=True)
		self.activationId = None


	def sendTracker(self):
		mqSender = parent.Guide.op('./mqout')
		tid = self.lampId
		gid = self.lampId
		x = self.trackerPosition['x'] #float(pars.Positionx.eval())
		y = self.trackerPosition['z'] #-float(pars.Positiony.eval())
		z = -1*self.trackerPosition['y'] #float(pars.Height.eval())
		msg = f'{x:.2f},{y:.2f},{z:.2f},{gid},Tracker:{tid}'
		mqSender.send(msg)



class LampManagerExt:
	"""
	This Extension is used to manage which lamps do what at what time...
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.lamps = {i: Lamp(i) for i in range(16)}

	def printOutLamps(self):
		return str(self.lamps).replace(',','\n') 


	def requestLamp(self, lampId, purpose):
		lamp = self.lamps[lampId]
		debug(lampId, lamp)
		if lamp.purpose:
			return None
		else:
			lamp.purpose = purpose
			return lamp

	def releaseLamp(self, lampId):
		lamp = self.lamps[lampId]
		lamp.purpose = None
		if lamp.activationId:
			lamp.deactivate()
		return

	def setLampTracker(self, lampId, position):
		lamp = self.lamps[lampId]
		lamp.trackerPosition = position

	def sendMQTracker(self):
		for lamp in self.lamps.values():
			lamp.sendTracker()
		return

	def releaseAll(self):
		for lampId in self.lamps:
			self.releaseLamp(lampId)
		return



	