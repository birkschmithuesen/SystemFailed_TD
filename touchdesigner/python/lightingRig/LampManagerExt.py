from lamp import Lamp

class LampManagerExt(dict):
	"""
	This Extension is used to manage which lamps do what at what time...
	"""
	lampTable = op.main.op('spikies')

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		for i in range(16):
			self[i] = Lamp(i, (float(LampManagerExt.lampTable[i, 2].val), float(LampManagerExt.lampTable[i, 3].val), float(LampManagerExt.lampTable[i, 4].val)))

	def PrintOutLamps(self):
		return str(self).replace(',','\n') 

	def Reset(self):
		debug("Resetting LampManger")
		self.releaseAll()

	def RequestLampById(self, requester, lampId):
		debug(requester, lampId)
		lamp = self[lampId]
		if not lamp.owner or requester.priority > lamp.owner.priority:
			if lamp.owner:
				lamp.owner.releaseLamp(lampId)
			requester.append(lamp)

	def RequestLamps(self, requester, amount):
		# 1. look for idle Lamps
		# 2. look for lamps with lower prio
		# 3. look for lamps with same prio (but automatically older)
		# and return them (and mark theam in a way)
		# if there are still lamps missing, add to queue (and eventually process the queue)
		for priority in (0, requester.priority, requester.priority + 1):
			print('priority', priority)
			missingAmount = amount - len(requester)
			for i in range(missingAmount):
				j0 = (i*math.floor(16/amount))%16
				lamp = None
				j = j0
				while not lamp and j < (j0+16):
					print('tesId', j%16)
					candidate = self[j%16]
					if not candidate.owner or (candidate.owner != requester) and priority > candidate.owner.priority:
						lamp = candidate
						if lamp.owner:
							# should we add this requester to a requestcue to give him back a lamp asap?
							lamp.owner.releaseLamp(lamp.lampId)
						requester.append(lamp)
						debug(f"appended lamp {lamp}")
					j += 1
		if len(requester) < amount:
			# should we add this requester to a requestcue to give him back a lamp asap?
			pass

	def releaseAll(self):
		for lampId in self:
			self[lampId].release()
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
