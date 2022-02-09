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

	def __repr__(self):
		return f"highlight for {self.trackid} / cue {self.cue} with lamps {[lamp.lampId for lamp in self.lamps]}"

class HighlighterExt:
	"""
	HighlighterExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.highlights = {}

	def reset(self):
		debug('resetting Highlighter')
		self.highlights = {}
		me.ext.LampManagerExt.releaseAll()
		return

	def printOutHighlights(self):
		return str(self.highlights).replace(',','\n')

	# whenever either a new ID appears or the highlightcue for an existing ID changes, we have to compose a new Highlight
	# composing an highlight consist of:
	# - choose one or more Lamps to track the ID
	# - send the respective trackers (continously)
	# - (maybe trigger a new composition after a second or so)
	# - trigger MQ-execs by osc
	def NewHighlight(self, highlight):
		debug(f'composing highlight for tracker {highlight.trackid}')
		i = 0
		lamp = None
		while not lamp and i < 16:
			lamp = me.ext.LampManagerExt.requestLamp(i, 'highlight')
			i += 1
		debug(f"got lamp {lamp}")
		cue_table = parent.Guide.op('cue_table')
		lamp.color = cue_table[highlight.cue, 'Color'].val
		lamp.beam = cue_table[highlight.cue, 'Beam'].val
		lamp.shutter = cue_table[highlight.cue, 'Shutter'].val
		activationId = cue_table[highlight.cue, 'Activation'].val
		debug(activationId)
		lamp.activate(activationId)
		highlight.lamps.append(lamp)
		self.highlights[highlight.trackid] = highlight
		return

	# whenever an ID disappears from the list or the highlightcue for an existing ID changes, we have to remove the former Highlight:
	# - turn MQ-execs off by osc
	def DeleteHighlight(self, highlightId):
		debug(f'Deleting Highlight {highlightId}')
		for lamp in self.highlights[highlightId].lamps:
			me.ext.LampManagerExt.releaseLamp(lamp.lampId)
		del self.highlights[highlightId]
		return

	# whenever the position values for an ID change, we have to change the position for the respective trackers
	def UpdatePosition(self, trackid, position):
		#return
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
			highlight = Highlight(row)
			if highlight.trackid == "Trackid":
				# the heading row...
				continue
			
			if highlight.trackid not in tempHighlights:
				# complete new Highlight!
				debug(f"{highlight} is completely new!")
				newHighlights.append(highlight)
				#self.NewHighlight(highlight)
			else:
				if tempHighlights[highlight.trackid].cue != highlight.cue:
					# this trackid has the cue changed - so it is considered new
					debug(f"{highlight} has a new cue-type!")
					newHighlights.append(highlight)
					#self.NewHighlight(highlight)
				else:
					# if this trackid had a highlight before AND had the same cue, it is considered already existent
					debug(f"{highlight} already there")

				del tempHighlights[highlight.trackid]
			
		for oldHighlight in tempHighlights:
			debug(f"deleting {tempHighlights[oldHighlight]}")
			self.DeleteHighlight(oldHighlight)

		for newHighlight in newHighlights:
			self.NewHighlight(newHighlight)

		debug("stop reIndex", self.highlights)
		return


