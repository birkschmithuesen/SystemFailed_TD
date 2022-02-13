def onPulse(par):
	op('traillock').lock = 0
	op('scalar_lock').lock = 0
	run("op('traillock').lock = 1", delayFrames = 1)
	run("op('scalar_lock').lock = 1", delayFrames = 1)
	return