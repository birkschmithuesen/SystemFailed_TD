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
			self.send(f'/sound/{subtype}', [int(trigger)])
		return

	def SendSoundLocalized(self, subtype, trigger = 1, posx = 0, posy = 0):
		if self.pars['Noises']:
			self.send(f'/sound/{subtype}', [int(trigger), float(posx), float(posy)])
		return

	def SendSynth(self, pitch = 1, level = 0, posx = 0, posy = 0):
		if self.pars['Synth']:
			self.Send(f'/synth/{int(pitch)}', [float(level), float(posx), float(posy)])
		return

	def SendTrackfail(self, pitch =1):
		self.Send(f'/sound/trackfail', [int(pitch)])
		return