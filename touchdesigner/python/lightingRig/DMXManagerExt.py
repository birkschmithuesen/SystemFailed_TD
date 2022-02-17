"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from inspect import signature

class DMXManagerExt(list):
	"""
	DMXManagerExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.initFromDmx()

	def initFromDmx(self):
		for i in range(512):
			value = op('dmxin1')[f'c{i+1}']
			print(i, value)
			self.append({'value':value, 'callbacks':[]})

	def updateDmxChannel(self, channel, value):
		#debug(channel, value)
		self[channel]['value'] = value
		for callback in self[channel]['callbacks']:
			self.executeCallback(channel, callback)

	def subscribeChannel(self, channel, callback, sixteenBit=False):
		#debug(callback)
		self[channel]['callbacks'].append(callback)
		self.executeCallback(channel, callback)

	def unsubscribeChannel(self, channel, callback):
		if callback in self[channel]['callbacks']:
			self[channel]['callbacks'].remove(callback)
		#debug(self[channel])

	def executeCallback(self, channel, callback):
		value = self[channel]['value']
		if len(signature(callback).parameters) == 1:
			callback(value)
		else:
			callback(channel, value)

	def Reset(self):
		self.clear()
		self.initFromDmx()