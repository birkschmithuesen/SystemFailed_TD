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
		self.MaxSlots = op.Settings.par.Maxtracks

		# TODO use reference to ownerComp parameter instead of fixed size to couple this to replicator configuration
		self.EmptySlots = set(range(1, 1 + self.MaxSlots))
		self.UnassignedIds = list()

	def Reassign(self):
		self.EmptySlots = set(range(1, 1 + self.MaxSlots))
		ad = op('active_dat')
		tmp = list(self.Assignment.keys())
		for tid in tmp:
			self.Unassign(tid)
		for row in ad.rows():
			if row[1].val:
				tid = row[0].val
				self.Assign(int(tid))

	def ResolveID(self, tid):
		try:
			return self.Assignment[tid]
		except KeyError:
			return False

	def Assign(self, tid):
		slot = self.ResolveID(tid)
		if not slot:
			debug(f"trying to assign {tid} to a new slot")
			if len(self.EmptySlots) <= 0:
				debug(f"unable to add tracker for id {tid} - no unassigned slots")
				slot = -1
			else:
				slot = self.EmptySlots.pop()
				self.Setup(slot, tid)
				# debug(f'Assigned {tid} to {slot}')
		return slot

	def Unassign(self, tid):
		try:
			slot = self.Assignment.pop(int(tid))
		except KeyError:
			slot = -1
			# debug(f"Unassign {tid} failed - assignment not found")
		else:
			self.Unset(slot, tid)
			# debug(f'Unassigned {tid} from {slot}')
		finally:
			return slot

	def Setup(self, slot, tid):
		slot = int(slot)
		tid = int(tid)
		
		self.Assignment[tid] = slot

		tracker = self.ownerComp.op(f'slot_{slot}')
		tracker.name = f'tracker_{tid}'
		tracker.par.Trackid = tid
		tracker.par.opshortcut = f'tracker_{tid}'
		tracker.par.Active = True
		# tracker.par.play = True

	def Unset(self, slot, tid):
		slot = int(slot)
		tid = int(tid)
		
		tracker = self.ownerComp.op(f'tracker_{tid}')
		tracker.name = f'slot_{slot}'
		tracker.par.Trackid = 0
		tracker.par.opshortcut = ''
		tracker.par.Active = False
		# tracker.par.play = False

		self.EmptySlots.add(slot)