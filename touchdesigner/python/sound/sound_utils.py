"""
TouchDesigner Utilities for SystemFailed Sound Component, 
mostly convenience wrappers for common OSC sound directives.
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

class Utils:
	"""
	Utils for the SystemFailed Sound comp
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.pars = ownerComp.par
		maxmsp1 = op('sender_maxmsp')
		maxmsp2 = op('sender_debug_maxmsp')
		ableton1 = op('sender_ableton')
		ableton2 = op('sender_debug_ableton')
		
		self.maxmspSenders = [maxmsp1, maxmsp2]
		self.abletonSenders = [ableton1, ableton2] 
		self.zaps = dict()
		self.zUnassigned = set(range(10))
		self.strobes = dict()
		self.sUnassigned = set(range(4))

	def SendMaxmsp(self, message, args):
		for s in self.maxmspSenders:
			# debug(f'{self.ownerComp} sending osc on {s}:\n {message}, {args}')
			s.sendOSC(message, args, asBundle=False, useNonStandardTypes=True)
		return

	def SendAbleton(self, message, args):
		for s in self.abletonSenders:
			# debug(f'{self.ownerComp} sending osc on {s}:\n {message}, {args}')
			s.sendOSC(message, args, asBundle=False, useNonStandardTypes=True)
		return

	def SendScene(self, name):
		msg = f'/scene'
		args = [str(name)]
		self.SendMaxmsp(msg, args)
		return

	def SendIntro(self, name):
		msg = f'/intro/{name}'
		args = [int(1)]
		self.SendAbleton(msg, args)
		return

	def SendVoice(self, subtype, arguments):
		msg = f'/voice/{subtype}'
		args = [int(a) for a in arguments]
		self.SendMaxmsp(msg, args)
		return

	def SendRound(self, subtype, arguments):
		msg = f'/round/{subtype}'
		args = [int(a) for a in arguments]
		self.SendAbleton(msg, args)
		return

	def SendFreeze(self, subtype, trackid):
		if self.pars['Freeze']:
			newType = f'freeze/{subtype}'
			self.SendVoice(newType, [trackid])
		return

	def SendBenched(self, subtype, trackid):
		if self.pars['Benched']:
			newType = f'benched/{subtype}'
			self.SendVoice(newType, [trackid])
		return

	def SendEvaluationStart(self, trigger = 1):
		self.SendRound('evaluation/start', [trigger])
		return

	def SendEvaluationRank(self, subtype, rank):
		newType = f'evaluation/{subtype}'
		hs = op('highscore_set')
		if subtype == 'high':
			ref = rank
		else:
			ref = hs.numSamples - rank
		trackid = hs['Trackid'][rank]
		score = hs['Newhighscore'][rank]
		self.SendVoice(newType, [trackid, score, rank])
		return

	def SendConformEnd(self, trigger = 1):
		self.SendRound('conformbehavior',[trigger])
		return

	def SendRebelEnd(self, trigger = 1):
		self.SendRound('rebelbehavior',[trigger])
		return

	def SendCountdown(self, trigger = 1):
		self.SendRound('countdown', [int(trigger)])
		return

	def SendSoundTrigger(self, subtype, trigger = 1):
		if self.pars['Noises']:
			self.SendAbleton(f'/sound/{subtype}', [int(trigger)])
		return

	def SendSoundLocalized(self, subtype, slot = 0, trigger = 1, posx = 0, posy = 0):
		if self.pars['Noises']:
			self.SendAbleton(f'/sound/{subtype}', [int(slot),int(trigger), float(posx), float(posy)])
		return

	def SendSynth(self, pitch = 1, level = 0, posx = 0, posy = 0):
		if self.pars['Synth']:
			self.SendMaxmsp(f'/synth', [int(pitch)+1, float(level), float(posx), float(posy)])
		return

	def SendTrackfail(self, pitch =1):
		self.SendAbleton(f'/sound/trackfail', [int(pitch)])
		return

	# list tracks: [trackid, px, py]
	def SendZaps(self, tracks):
		tmp = dict()
		deletes = set()
		zaps = self.zaps

		if len(tracks) > 1:
			for track in tracks:
				tid = track[0]
				tx = track[1]
				ty = track[2]
				tmp[tid] = (tid,tx,ty)
		for tid in tmp.keys():
			# vals = tmp[tid]
			if tid in zaps.keys():
				# RETRIGGER
				slotid = zaps[tid][0]
				zaps[tid] = (slotid, tmp[tid][0], tmp[tid][1], tmp[tid][2])
				debug(f'zap retrigger {zaps[tid]}')
				self.SendSoundLocalized(subtype='zap', slot=slotid, trigger=-1, posx=zaps[tid][2], posy=zaps[tid][3])
			else: 
				if len(self.zUnassigned) == 0:
					pass
				# TRIGGER
				slotid = self.zUnassigned.pop()
				zaps[tid] = (slotid, tmp[tid][0], tmp[tid][1], tmp[tid][2])
				debug(f'zap trigger {zaps[tid]}')
				self.SendSoundLocalized(subtype='zap', slot=slotid, trigger=1, posx=zaps[tid][2], posy=zaps[tid][3])
		for tid in zaps.keys():
			if not (tid in tmp.keys()):
				deletes.add(tid)
		for tid in deletes:
			# OFF
			self.SendSoundLocalized(subtype='zap', slot=zaps[tid][0], trigger=0, posx=zaps[tid][2], posy=zaps[tid][3])
			self.zUnassigned.add(zaps[tid][0])
			zaps.pop(tid)

	def SendStrobes(self, tracks):
		tmp = dict()
		deletes = set()
		strobes = self.strobes
		for track in tracks:
			tid = track[0]
			tx = track[1]
			ty = track[2]
			tmp[tid] = (tid,tx,ty)
		for k in strobes.keys():
			if not k in tmp.keys():
				deletes.add(k)
		for k in deletes:
			# OFF
			self.SendSoundLocalized(subtype='strobe', slot=k, trigger=0, posx=zaps[k][1], posy=zaps[k][2])
			strobes.pop(k)
			self.sUnassigned.add(k)
			pass
		for k in tmp.keys():
			if len(self.zUnassigned) == 0:
				break
			vals = tmp[k]
			if k in strobes.keys():
				# RETRIGGER
				slotid = strobes[k][0]
				strobes[k] = (slotid, tmp[k][0], tmp[k][1], tmp[k][2])
				self.SendSoundLocalized(subtype='strobe', slot=k, trigger=1, posx=zaps[k][1], posy=zaps[k][2])
			else: 
				# TRIGGER
				slotid = self.sUnassigned.pop()
				strobes[k] = (slotid, tmp[k][0], tmp[k][1], tmp[k][2])
				self.SendSoundLocalized(subtype='strobe', slot=k, trigger=1, posx=zaps[k][1], posy=zaps[k][2])
