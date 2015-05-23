import time

#this is the map with all the variables that user can change. All must be set at all times!

class Changables:
	#display variables
	FrameW = 800
	FrameH = 800

	TextSize = 36

	#Train Start, end location
	TrainStart = "Ljubljana"
	TrainStop = "Ljubljana-Zalog"
	

	#Bus number, station, direction
	BusNum = 11
	BusStation = "Zadruzni"
	BusDirection = "Be\u017eigrad"

	#How many trains/buses do you want to skip on your timeline. You can change this in the program, this is here just for sync and starting variable.
	Skip = 0

	#train and bus pic transformation koeficients
	PicWCOF = int(FrameW/5)
	PicHCOF = int(FrameH/4) 
