# me - this DAT.
# 
# dat - the changed DAT
# rows - a list of row indices
# cols - a list of column indices
# cells - the list of cells that have changed content
# prev - the list of previous string contents of the changed cells
# 
# Make sure the corresponding toggle is enabled in the DAT Execute DAT.
# 
# If rows or columns are deleted, sizeChange will be called instead of row/col/cellChange.

# PATCH
# per Head 1...27
# 23: Zoom
# 24: Zoom F
# 26: Intensity
# 27: Intensity Fine


def onTableChange(dat):
	print(absTime.frame)
	#op.DMX.ext.DMXManagerExt.updateData(dat)
	print(op('dmxin1')[0])
	return

def onRowChange(dat, rows):
	return

def onColChange(dat, cols):
	return

def onCellChange(dat, cells, prev):
	for cell in cells:
		channel = cell.col-1 	# zero-based!
		#print(f'channel {channel} @ {cell.val}')
		head = math.floor(channel/27)
		chan = channel%27
	
		# set intensity-channels
		if chan == 25 and head <10:
			op('lamps').ext.HighlighterExt.setAttributeForHighlightCue('intensity', head+1, int(cell.val)/255)
		# set zoom
		if chan == 22 and head <10:
			op('lamps').ext.HighlighterExt.setAttributeForHighlightCue('zoom', head+1, int(cell.val)/255)

		if channel in range(400,416):
			#print(f'channel {channel} @ {cell.val}')
			op('lamps').ext.LampManagerExt.setReservationForLamp(channel-400, int(cell.val)/255)

	return

def onSizeChange(dat):
	return
	