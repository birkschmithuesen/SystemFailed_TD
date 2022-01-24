# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):	
	osc = parent.Guide.op('./oscout')
	gid = parent.mqguide.par.Guideid
	table = op('cue_table')

	for c in changes:
		par = c.par
		prev = c.prev
		if par.name == 'Cue' and par.eval() == 0:
			#turn previous exec off
			cue = str(prev)
			level = 0
			break
		elif par.name == 'Level':
			#change level only
			cue = str(parent.mqguide.par.Cue.eval())
			level = float(table[str(gid),'Intensity'].val) * float(parent.mqguide.par.Level.eval())
		else:
			#new cue, send full look
			cue = par.eval()
			color = op('cue_table')[str(gid),'Color'].val
			beam = op('cue_table')[str(gid),'Beam'].val
			shutter = op('cue_table')[str(gid),'Shutter'].val
			color_ex = f'/exec/14/{color}'
			beam_ex = f'/exec/12/{beam}'
			shut_ex = f'/exec/12/{shutter}'
			osc.sendOSC(ex_ref, [int(100)], useNonStandardTypes=True)
			osc.sendOSC(ex_ref, level, useNonStandardTypes=True)
			osc.sendOSC(ex_ref, level, useNonStandardTypes=True)
		pass
	#send level (including activation/deactivation) _once exactly_ per active frame
	act = table[str(cue), 'Activation'].val
	act_ex = str(act+gid)
	osc.sendOSC(act_ex, [float(level)], useNonStandardTypes=True)
	return

def onPulse(par):
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	