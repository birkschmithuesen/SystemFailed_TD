# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	rt = me.parent.Roundtimer
	name = par.name
	val = par.eval()
	if name == 'Play':
		if val:
			rt.Play()
		else:
			rt.Pause()
	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
	return

def onPulse(par):
	rt = me.parent.Roundtimer
	name = par.name
	if name == 'Reinit':
		rt.ReInit()
	elif name == 'Gointro':
		rt.GoIntro()
	elif name == 'Endintro':
		rt.EndIntro()
	elif name == 'Goround':
		rt.GoRound()
	elif name == 'Endround':
		rt.EndRound()
	elif name == 'Gooutro':
		rt.GoOutro()
	elif name == 'Endoutro':
		rt.EndOutro()
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	