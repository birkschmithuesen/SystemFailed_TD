"""
This extension provides utility functions for the trackers
	- id and status assignment
"""

from TDStoreTools import StorageManager, DependList, DependDict

import TDFunctions as TDF

class Utils:
	"""
	Utils description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		self.TrackIds = DependList()
		self.Assignment = DependDict()

		# TODO use reference to ownerComp parameter instead of fixed size to couple this to replicator configuration
		self.EmptySlots = set(range(1,51))
		self.UnassignedIds = list()

	def Reassign(self):
		self.EmptySlots = set(range(1,51))
		ad = op('active_dat')
		tmp = list(self.Assignment.keys())
		for i in range(1,51):
			tslot = op(f'tracker_{i}')
			tslot.par.Trackid = 0
			tslot.par.Active = 0
		for tid in tmp:
			self.Unassign(tid)
		for row in ad.rows():
			tid = row[0].val
			debug(tid)
			self.Assign(int(tid))

	def ResolveID(self, tid):
		try:
			return self.Assignment[tid]
		except KeyError:
			return False

	def Assign(self, tid):
		slot = self.ResolveID(tid)
		if not slot:
			if len(self.EmptySlots) <= 0:
				debug(f"unable to add tracker for id {tid} - no unassigned slots")
				slot = -1
			else:
				slot = self.EmptySlots.pop()
				self.Assignment[tid] = slot
				tracker = self.ownerComp.op(f'tracker_{slot}')
				tracker.par.Trackid = tid
				self.Setup(slot)
				debug(f'Assigned {tid} to {slot}')
		return slot

	def Unassign(self, tid):
		try:
			slot = self.Assignment.pop(int(tid))
		except KeyError:
			# debug(f"Unassign {tid} failed - assignment not found")
			slot = -1
		else:
			tracker = self.ownerComp.op(f'tracker_{slot}')
			tracker.par.Trackid = 0
			self.Setup(slot)
			self.EmptySlots.add(slot)
			debug(f'Unassigned {tid} from {slot}')
		finally:
			return slot

	def Setup(self, slot):
		slot = int(slot)
		tracker = self.ownerComp.op(f'tracker_{slot}')
		tid = int(tracker.par.Trackid)
		if tid:
			tracker.par.Active = True
		else:
			tracker.par.Active = False