"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

class Lamp:
	def __init__(self, lampId, position):
		self.oscSender = parent.Guide.op('./oscout')
		self.lampId = lampId
		self.activated = False
		self.position = position
		# get from DMX-Values
		dmxTable = parent.Guide.op('dmx_table')
		self.purpose = "MQ" if int(dmxTable[1, self.lampId+400].val) == 0 else None
		self.purposeId = None
		self.zoom = 0.5
		self.intensity = 1.0
		self.activationId = 0
		self.trackerPosition = {'x':0, 'y':0, 'z':0}
		self.color = 0
		self.beam = 0
		self.shutter = 0
		self.oscThrottelCounter = 0

	def __repr__(self):
		return f"lamp#{self.lampId} has purpose {self.purpose}#{self.purposeId}"

	def dist(self, a, b):
		return math.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2)

	@property
	def trackerPosition(self):
		return self._trackerPosition
	
	@trackerPosition.setter
	def trackerPosition(self, value):
		self._trackerPosition = value
		# calculate distance to tracker
		dist = 1000 * self.dist(value, self.position)

		# calculate zoom to achieve size (r = 1200mm...75mm)
		# spikie zoom 27°...4°
		#  tan (alpha/2) = r/dist
		# alpha = 2 * atan (r/dist)
		r = 1200 - self.zoom * (1200-75)
		alpha = 2 * math.atan(r/dist) / math.pi * 180
		debug(dist, r, alpha)
		if alpha > 27:
			zoomFactor = 0.0
		elif alpha < 4:
			zoomFactor = 1.0
		else:
			zoomFactor = ((27-alpha)/23)

		# set size (if activated)
		if self.activated:
			self.oscThrottelCounter += 1
			if self.oscThrottelCounter%2 == 0:			
				zoom_ex = f'/exec/15/{self.lampId+1}'
				debug(zoom_ex, [self._zoom*zoomFactor*0.999999], self.zoom, zoomFactor)
				#if we send 1.0 the value in MQ is going to 0
				self.oscSender.sendOSC(zoom_ex, [self._zoom*zoomFactor*0.999999], useNonStandardTypes=True)
		return

	@property
	def color(self):
		return self._colorId

	@color.setter
	def color(self, value):
		self._colorId = value
		oscMessage = f'/exec/14/{int(value) + self.lampId}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)

	@property
	def shutter(self):
		return self._shutterId

	@shutter.setter
	def shutter(self, value):
		self._shutterId = value
		oscMessage = f'/exec/12/{int(value) + self.lampId}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)

	@property
	def beam(self):
		return self._beamId

	@beam.setter
	def beam(self, value):
		self._beamId = value
		oscMessage = f'/exec/12/{int(value) + self.lampId}'
		self.oscSender.sendOSC(oscMessage, [int(100)], useNonStandardTypes=True)

	@property
	def intensity(self):
		return self._intensity

	@intensity.setter
	def intensity(self, value):
		value = float(value)
		if value > 1.0:
			value = 1.0
		self._intensity = value
		if self.activated: 
			self.activate()

	@property
	def zoom(self):
		return self._zoom

	@zoom.setter
	def zoom(self, value):
		value = float(value)
		if value > 1.0:
			value = 1.0
		self._zoom = value
		if self.activated: 
			# TODO: call zoom-executor
			pass

	@property
	def activationId(self):
		return self._activationId

	@activationId.setter
	def activationId(self, value):
		if value:
			self._activationId = int(value)
		else:
			self._activationId = 0

	def activate(self):
		act_ex = f'/exec/13/{self.activationId + self.lampId}'
		debug("x",act_ex)
		#self.oscSender.sendOSC(act_ex, [self.intensity], useNonStandardTypes=True)
		self.oscSender.sendOSC(act_ex, [int(100)], useNonStandardTypes=True)
		parent.Guide.op('./oscout1').sendOSC(act_ex, [int(100)], useNonStandardTypes=True)
		self.activated = True

	def deactivate(self):
		act_ex = f'/exec/13/{self.activationId + self.lampId}'
		self.oscSender.sendOSC(act_ex, [0], useNonStandardTypes=True)
		parent.Guide.op('./oscout1').sendOSC(act_ex, [0], useNonStandardTypes=True)
		self.activated = False

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
		self.lampTable = parent.Guide.op('spikies')
		self.lamps = {i: Lamp(i, {'x':float(self.lampTable[i, 2].val), 'y':float(self.lampTable[i, 3].val), 'z':float(self.lampTable[i, 4].val)}) for i in range(16)}

	def printOutLamps(self):
		return str(self.lamps).replace(',','\n') 


	def requestLamp(self, lampId, purpose, purposeId):
		lamp = self.lamps[lampId]
		# debug(lampId, lamp)
		if lamp.purpose:
			return None
		else:
			lamp.purpose = purpose
			lamp.purposeId = purposeId
			return lamp

	def releaseLamp(self, lampId):
		lamp = self.lamps[lampId]
		if (lamp.purpose != "MQ"):
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

	# to be called from the DMX-filter:
	# value > 0 -> use for anything
	# value = 0 -> don't use! MQ wants it
	# TODO: when lamp has a purpose at the moment, find a replacement
	def setReservationForLamp(self, lampId, value):
		debug(lampId, value)
		lamp = self.lamps[lampId]
		debug(lamp)
		if lamp.purpose == "MQ" and value > 0:
			lamp.purpose = None
			lamp.purposeId = 0
		if lamp.purpose != "MQ" and value == 0:
			if lamp.purpose == "highlight":
				me.ext.HighlighterExt.releaseLamp(lampId)
			lamp.purpose = "MQ"
			lamp.purposeId = 0




	