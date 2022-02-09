# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
	return

def onCreate():
	return

def onExit():
	return

def onFrameStart(frame):
	op('text1').par.text = me.ext.HighlighterExt.printOutHighlights() + "\n\n" + me.ext.LampManagerExt.printOutLamps()
	return

def onFrameEnd(frame):
	me.ext.LampManagerExt.sendMQTracker()
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	return

	