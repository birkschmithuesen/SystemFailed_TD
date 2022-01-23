# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
	mqSender = parent.Guide.op('./mqout')
	pars = parent.guideslot.par
	tid = int(pars.Trackid.eval())
	gid = int(pars.Guideid.eval())
	x = float(pars.Positionx.eval())
	y = -float(pars.Positiony.eval())
	z = float(pars.Height.eval())
	msg = f'{x:.2f},{z:.2f},{y:.2f},{gid},Tracker:{tid}'
	mqSender.send(msg)
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
	