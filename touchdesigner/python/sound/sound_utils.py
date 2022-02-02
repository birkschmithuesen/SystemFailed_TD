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
		osc1 = op('sender')
		osc2 = op('sender_debug')
		self.oscSenders = [osc1, osc2]
		self.zaps = dict()
		self.zUnassigned = set(range(10))
		self.strobes = dict()
		self.sUnassigned = set(range(4))

	def Send(self, message, args):
		for s in self.oscSenders:
			# debug(f'{self.ownerComp} sending osc on {s}:\n {message}, {args}')
			s.sendOSC(message, args, asBundle=False, useNonStandardTypes=True)
		return

	def SendScene(self, name):
		msg = f'/scene'
		args = [str(name)]
		self.Send(msg, args)
		return

	def SendIntro(self, name):
		msg = f'/intro/{name}'
		args = [int(1)]
		self.Send(msg, args)
		return

	def SendVoice(self, subtype, arguments):
		msg = f'/voice/{subtype}'
		args = [int(a) for a in arguments]
		self.Send(msg, args)
		return

	def SendFriendly(self, trackid, score):
		if self.pars['Warning']:
			self.SendVoice('friendly', [trackid, score])
		return

	def SendFreeze(self, subtype, trackid, score):
		if self.pars['Freeze']:
			newType = f'freeze/{subtype}'
			self.SendVoice(newType, [trackid, score])
		return

	def SendBenched(self, subtype, trackid, score):
		if self.pars['Benched']:
			newType = f'benched/{subtype}'
			self.SendVoice(newType, [trackid, score])
		return

	def SendEvaluationStart(self, trigger = 1):
		self.SendVoice('evaluation/start', [trigger])
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
		self.SendVoice('conformbehaviour',[trigger])
		return

	def SendRebelEnd(self, trigger = 1):
		self.SendVoice('rebelbehaviour',[trigger])
		return

	def SendCountdown(self, trigger = 1):
		self.Send('/round/countdown', [int(trigger)])
		return

	def SendSoundTrigger(self, subtype, trigger = 1):
		if self.pars['Noises']:
			self.Send(f'/sound/{subtype}', [int(trigger)])
		return

	def SendSoundLocalized(self, subtype, slot = 0, trigger = 1, posx = 0, posy = 0):
		if self.pars['Noises']:
			self.Send(f'/sound/{subtype}', [int(slot),int(trigger), float(posx), float(posy)])
		return

	def SendSynth(self, pitch = 1, level = 0, posx = 0, posy = 0):
		if self.pars['Synth']:
			self.Send(f'/synth', [int(pitch), float(level), float(posx), float(posy)])
		return

	def SendTrackfail(self, pitch =1):
		self.Send(f'/sound/trackfail', [int(pitch)])
		return

	# list tracks: [trackid, px, py]
	def SendZaps(self, tracks):
		tmp = dict()
		deletes = set()
		zaps = self.zaps
		for track in tracks:
			tid = track[0]
			tx = track[1]
			ty = track[2]
			tmp[tid] = (tid,tx,ty)
		for k in zaps.keys():
			if not k in tmp.keys():
				deletes.add(k)
		for k in deletes:
			self.SendSoundLocalized(subtype='zap', slot=k, trigger=0, posx=zaps[k][1], posy=zaps[k][2])
			zaps.pop(k)
			self.zUnassigned.add(k)
			pass
		for k in tmp.keys():
			if len(self.zUnassigned) == 0:
				break
			vals = tmp[k]
			if k in zaps.keys():
				slotid = zaps[k][0]
			else: 
				slotid = self.zUnassigned.pop()
			zaps[k] = (slotid, tmp[k][0], tmp[k][1], tmp[k][2])
		for k in zaps:
			self.SendSoundLocalized(subtype='zap', slot=k, trigger=1, posx=zaps[k][1], posy=zaps[k][2])

	def SendStrobes(self, tracks):
		tmp = dict()
		deletes = set()
		zaps = self.zaps
		for track in tracks:
			tid = track[0]
			tx = track[1]
			ty = track[2]
			tmp[tid] = (tid,tx,ty)
		for k in zaps.keys():
			if not k in tmp.keys():
				deletes.add(k)
		for k in deletes:
			self.SendSoundLocalized(subtype='zap', slot=k, trigger=0, posx=zaps[k][1], posy=zaps[k][2])
			zaps.pop(k)
			self.zUnassigned.add(k)
			pass
		for k in tmp.keys():
			if len(self.zUnassigned) == 0:
				break
			vals = tmp[k]
			if k in zaps.keys():
				slotid = zaps[k][0]
			else:
				slotid = self.zUnassigned.pop()
			zaps[k] = (slotid, tmp[k][0], tmp[k][1], tmp[k][2])
		for k in zaps:
			self.SendSoundLocalized(subtype='zap', slot=k, trigger=1, posx=zaps[k][1], posy=zaps[k][2])