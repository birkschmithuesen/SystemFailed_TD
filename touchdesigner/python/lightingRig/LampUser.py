class LampUser(list):
	counter = 0

	def __init__(self):
		self.priority = 0
		self.cntId = LampUser.counter
		LampUser.counter += 1

	def append(self, lamp):
		lamp.owner = self
		super().append(lamp)

	def delete(self):
		self.releaseAllLamps()
		# more cleanup to be done???

	def releaseLamp(self, lampId):
		lamp = self.getLampById(lampId)
		if lamp:
			lamp.release()
			self.remove(lamp)

	def releaseAllLamps(self):
		for lamp in self:
			lamp.release()
		self.clear()

	def getLampById(self, lampId):
		for lamp in self:
			if lamp.lampId == lampId:
				return lamp
		else:
			return None
	
class MQLampControll(LampUser):
	def __repr__(self):
		return "MagicQ"
