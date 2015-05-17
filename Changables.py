import time

#this is the map with all the variables that user can change

class Changables:
	#display variables
	FrameW = 800
	FrameH = 800

	TextSize = 36

	#Start, end location
	TrainStart = "Ljubljana-Zalog"
	TrainStop = "Ljubljana"
	SkipTrains = 0

	#train and bus pic transformation koeficients
	PicWCOF = int(FrameW/5)
	PicHCOF = int(FrameH/4) 
