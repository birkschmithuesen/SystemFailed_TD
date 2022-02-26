class Lamp:
	magicQ = op.magicQ

	def __init__(self, lampId, position):
		self.lampId = lampId
		self.activationId = None
		self.trackerId = 0
		self.intensity = 0
		self.beamSize = 0
		self.position = position
		self.trackerPosition = (0,0,0)
		self.zoom = 0
		self.owner = None
		self.dist = 0
		
	####### PROPERTIES

	@property
	def owner(self):
		return self._owner

	@owner.setter
	def owner(self, value):
		self._owner = value

	@property
	def intensity(self):
		return self._intensity

	@intensity.setter
	def intensity(self, value):
		#debug(value)
		value = float(value)
		if value > 1.0:
			value = 1.0
		self._intensity = value
		if self.activationId == 66:
			Lamp.magicQ.SetActivationViaArtnet(self.activationId, self.intensity, self.lampId)
		elif self.activationId:
			Lamp.magicQ.SetActivation(self.activationId, self.intensity, self.lampId)

	@property
	def zoom(self):
		return self._zoom

	@zoom.setter
	def zoom(self, value):
		if isinstance(value, int):
			value = value/255
		if hasattr(self, '_zoom') and value == self.zoom: 
			return
		value = float(value)
		if value > 1.0:
			value = 1.0
		self._zoom = value
		if self.intensity > 0:
			Lamp.magicQ.SetZoom(self.lampId, value)

	@property
	def activationId(self):
		return self._activationId

	@activationId.setter
	def activationId(self, value):
		if value:
			self._activationId = int(value)
		else:
			# TODO: what is this for?
			self._activationId = 0

	@property
	def trackerPosition(self):
		return self._trackerPosition
	
	@trackerPosition.setter
	def trackerPosition(self, value):
		self._trackerPosition = value
		if self.beamSize > 0:
			self.calculateZoomFromBeamSize()
		self.setMQTracker()

	@property
	def beamSize(self):
		return self._beamSize

	@beamSize.setter
	def beamSize(self, value):
		self._beamSize = value
		if self.beamSize > 0:
			self.calculateZoomFromBeamSize()

	@property
	def color(self):
		return self._colorId

	@color.setter
	def color(self, value):
		self._colorId = value
		Lamp.magicQ.ChooseSoftPalette('color', int(value), self.lampId)

	@property
	def shutter(self):
		return self._shutterId

	@shutter.setter
	def shutter(self, value):
		self._shutterId = value
		Lamp.magicQ.ChooseSoftPalette('shutter', int(value), self.lampId)

	@property
	def beam(self):
		return self._beamId

	@beam.setter
	def beam(self, value):
		self._beamId = value
		Lamp.magicQ.ChooseSoftPalette('beam', int(value), self.lampId)


	############ "PRIVATE" METHODS


	def setMQTracker(self):
		Lamp.magicQ.SetTracker(self.lampId, self.trackerId, self.trackerPosition)

	def calculateZoomFromBeamSize(self):
		# calculate distance to tracker - all positions in m
		a = self.trackerPosition
		b = self.position
		dist = 100 * math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
		self.dist = dist
		if dist == 0 or self.beamSize == 0:
			return

		self.zoom = self.dmxValue(self.beamSize*200, dist)/255
		#debug(self.zoom)

	def dmxValue(self, size, distance):
		# size in cm
		# distance in cm
		size1cm = size/distance
		out = 216.73*size1cm**2 - 710.8*size1cm + 305.84
		if out < 0: out = 0
		if out > 255: out = 255
		return out

	############ "PUBLIC" METHODS


	def __repr__(self):
		return f"lamp#{self.lampId} bz={self.beamSize:.1f} d={self.dist:.1f} z={self.zoom:.2f} owned by {self.owner}"

	def release(self):
		self.owner = None
		self.intensity = 0

	def setControllableFromDmx(self, value):
		self.controllable = value

