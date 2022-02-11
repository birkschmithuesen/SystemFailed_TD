"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

class Highlight:
	def __init__(self, row):
		self.trackid = row[0].val
		self.cue = row[16].val
		self.position = {'x': row[6].val, 'y': row[5].val, 'z': row[7].val}
		self.lamps = []
		self._intensity = 0
		# get from DMX-Values
		dmxTable = parent.Guide.op('dmx_table')
		self.intensity = int(dmxTable[1, (int(self.cue)-1)*27+26].val)/255.0
		self.activationId = None
		self.zoom = int(dmxTable[1, (int(self.cue)-1)*27+23].val)/255.0

	def __repr__(self):
		return f"highlight for {self.trackid} / cue {self.cue} with lamps {[lamp.lampId for lamp in self.lamps]} @ {float(self.intensity):.2f}/{float(self.zoom):.2f}"
	
	@property
	def intensity(self):
		return self._intensity

	@intensity.setter
	def intensity(self, value):
		prev = self._intensity
		if value == prev:
			return
		self._intensity = value
		for lamp in self.lamps:
			lamp.intensity = value
		if value == 0:
			self.releaseLamps()
		if prev == 0:
			self.acquireLamps()

	@property
	def zoom(self):
		return self._zoom

	@zoom.setter
	def zoom(self, value):
		self._zoom = value
		for lamp in self.lamps:
			lamp.zoom = value

	def acquireLamps(self):
		# TODO this can be nicer and more INTELLIGENT!
		debug(f'composing highlight for tracker {self.trackid}')
		amount = 1 if int(self.cue) < 6 else 2
		for i in range(amount):
			j = (i*math.floor(16/amount))%16
			lamp = None
			# TODO: ask for every lamp in the order of priority, not just up to nr.16
			while not lamp and j < 16:
				lamp = me.ext.LampManagerExt.requestLamp(j, 'highlight', self.trackid)
				j += 1
			debug(f"got lamp {lamp}")
			if lamp:
				self.lamps.append(lamp)
			self.setLampsFromCueTable()
			self.updateLamps()


	def setLampsFromCueTable(self):
		cueTable = parent.Guide.op('cue_table')
		for lamp in self.lamps:
			lamp.color = cueTable[self.cue, 'Color'].val
			lamp.beam = cueTable[self.cue, 'Beam'].val
			lamp.shutter = cueTable[self.cue, 'Shutter'].val
			lamp.activationId = cueTable[self.cue, 'Activation'].val

	def updateLamps(self):
		for lamp in self.lamps:
			lamp.intensity = self.intensity
			lamp.activate()

	def releaseLamp(self, lampId):
		debug(lampId)
		for lamp in self.lamps:
			if lamp.lampId == lampId:
				me.ext.LampManagerExt.releaseLamp(lamp.lampId)
				self.lamps.remove(lamp)

	def releaseLamps(self):
		for lamp in self.lamps:
			me.ext.LampManagerExt.releaseLamp(lamp.lampId)
		self.lamps.clear()


class HighlighterExt:
	"""
	HighlighterExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.highlights = {}
		
		self.cueTable = parent.Guide.op('cue_table')
		self.cueAttributes = {}
		# init the cue intensities with the value from the cue_table 
		# these intensities will later be set by dmx
		for row in self.cueTable.rows():
			if row[0].val == "Cue": 
				continue
			self.cueAttributes[int(row[0].val)] = {'intensity': self.cueTable[row[0].val, 'Intensity'].val, 'zoom': 1.0}

	def reset(self):
		debug('resetting Highlighter')
		self.highlights = {}
		me.ext.LampManagerExt.releaseAll()
		return

	def printOutHighlights(self):
		out = ""
		for highlight in self.highlights.values():
			out += str(highlight) + "\n"
		return out

	def releaseLamp(self, lampId):
		lamp = me.ext.LampManagerExt.lamps[lampId]
		highlight = self.highlights[lamp.purposeId]
		if highlight:
			highlight.releaseLamp(lampId)


	# to be called from the DMX-filter:
	def setAttributeForHighlightCue(self, attributeName, cueId, value):
		self.cueAttributes[cueId][attributeName] = value
		for highlight in self.highlights.values():
			if int(highlight.cue) == int(cueId):
				setattr(highlight, attributeName, value)

	# whenever either a new ID appears or the highlightcue for an existing ID changes, we have to compose a new Highlight
	# composing an highlight consist of:
	# - choose one or more Lamps to track the ID
	# - send the respective trackers (continously)
	# - (maybe trigger a new composition after a second or so)
	# - trigger MQ-execs by osc
	def NewHighlight(self, highlight):
		if highlight.trackid in self.highlights:
			self.DeleteHighlight(highlight.trackid)
		
		self.highlights[highlight.trackid] = highlight
		return

	# whenever an ID disappears from the list or the highlightcue for an existing ID changes, we have to remove the former Highlight:
	# - turn MQ-execs off by osc
	def DeleteHighlight(self, highlightId):
		debug(f'Deleting Highlight {highlightId}')
		self.highlights[highlightId].releaseLamps()
		del self.highlights[highlightId]
		return

	# whenever the position values for an ID change, we have to change the position for the respective trackers
	def UpdatePosition(self, trackid, position):
		if trackid not in self.highlights:
			return
		highlight = self.highlights[trackid]
		if not highlight:
			return
		for lamp in highlight.lamps:
			lamp.trackerPosition = position
		return


# this shit is needed to get from the Table to python objects...

	def reIndexHighlightsFromDat(self, dat):
		debug ("start reIndex", self.highlights)
		# go thru the rows and find out if it is a new highlight or a known one and also look if old ones don't exist anymore
		tempHighlights = dict(self.highlights)
		newHighlights = []

		for row in dat.rows():
			if row[0].val in ["Trackid", "0"]:
				# the heading row...
				continue
			highlight = Highlight(row)
			
			if highlight.trackid not in tempHighlights:
				# complete new Highlight!
				# debug(f"{highlight} is completely new!")
				newHighlights.append(highlight)
			else:
				if tempHighlights[highlight.trackid].cue != highlight.cue:
					# this trackid has the cue changed - so it is considered new
					# debug(f"{highlight} has a new cue-type!")
					newHighlights.append(highlight)
				else:
					# if this trackid had a highlight before AND had the same cue, it is considered already existent
					# debug(f"{highlight} already there")
					pass

				del tempHighlights[highlight.trackid]
			
		for oldHighlight in tempHighlights:
			# debug(f"deleting {tempHighlights[oldHighlight]}")
			self.DeleteHighlight(oldHighlight)

		for newHighlight in newHighlights:
			self.NewHighlight(newHighlight)

		debug("stop reIndex", self.highlights)
		return


