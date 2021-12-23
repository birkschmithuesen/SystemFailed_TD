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

	def ResolveID(self, tid):
		try:
			return self.Assignment[tid]
		except KeyError:
			return False

	def AssignTracker(self, tid):
		if len(self.EmptySlots) <= 0:
			debug(f"unable to add tracker for id {tid} - no unassigned slots")
			return -1
		slot = self.ResolveID(tid)
		if not slot:
			slot = EmptySlots.pop(0)
			Assignment[tid] = slot
			tracker = self.ownerComp.op(f'tracker_{slot}')
			#TODO use an actual activation&deactivation method on the tracker
			tracker.par.Active = True
			tracker.par.Trackid = tid
		return slot

	def UnassignTracker(self, tid):
		try:
			slot = self.Assignment.pop(tid)
		except KeyError:
			debug(f"Unassign {tid} failed - assignment not found")
			slot = None
		else:
			EmptySlots.add(slot)
			tracker = self.ownerComp.op(f'tracker_{slot}')
			#TODO use an actual activation&deactivation method on the tracker
			tracker.par.Active = False
			tracker.par.Trackid = 0
		finally:
			return slot
