import pygame
from pygame.locals import *
from Changables import *
from VozniRed2 import *


import time


class HIDvisuals:
	global CH 
	CH = Changables()

	OLDKeyPress = 0
	ToReturn = 0


	def Init(self):

		pygame.init()
		pygame.display.set_caption('IOTGUI')

		self.screen=pygame.display.set_mode((CH.FrameW, CH.FrameH))


		self.FONT = pygame.font.Font(None,CH.TextSize)

		#pic import and transform
		self.BusPic = pygame.image.load('Bus.png')
		self.BusPic = pygame.transform.scale(self.BusPic, (CH.PicWCOF, CH.PicHCOF))
		self.TrainPic = pygame.image.load('Train.png')
		self.TrainPic = pygame.transform.scale(self.TrainPic, (CH.PicWCOF, CH.PicHCOF))

		#stops text render
		self.TrainStartText = self.FONT.render(CH.TrainStart, 1, (255, 255, 255))
		self.TStartTextpos = self.TrainStartText.get_rect()
		self.TrainStopText = self.FONT.render(CH.TrainStop, 1, (255, 255, 255))
		self.TStopTextpos = self.TrainStopText.get_rect()



	def UserActions(self):
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
				self.OLDKeyPress = self.ToReturn = event.key
				
			if (event.type == KEYUP):
				if (event.key==self.OLDKeyPress):
					self.ToReturn = 0
		
		return self.ToReturn


	def Frame(self, NextTrain):
		self.screen.fill((0,0,0))

		#position the pictures
		self.screen.blit(self.BusPic,(CH.FrameW/2-CH.PicWCOF/2,CH.FrameH/4-CH.PicHCOF/2))
		self.screen.blit(self.TrainPic,(CH.FrameW/2-CH.PicWCOF/2,3*CH.FrameH/4-CH.PicHCOF/2))

		# train position stops Text
		Tx = self.TStartTextpos.centerx
		Ty = self.TStartTextpos.centery
		self.screen.blit(self.TrainStartText,(CH.FrameW/4-Tx, 2*CH.FrameH/3-Ty))
		Tx = self.TStopTextpos.centerx
		Ty = self.TStopTextpos.centery
		self.screen.blit(self.TrainStopText,(3*CH.FrameW/4-Tx, 2*CH.FrameH/3-Ty))

		# train time text
		self.TDepTime = self.FONT.render(NextTrain[0], 1, (255, 255, 255))
		self.TDepTextpos = self.TDepTime.get_rect()

		self.TArrTime = self.FONT.render(NextTrain[1], 1, (255, 255, 255))
		self.TArrTextpos = self.TArrTime.get_rect()

		Tx = self.TDepTextpos.centerx
		Ty = self.TDepTextpos.centery
		self.screen.blit(self.TDepTime,(CH.FrameW/4-Tx,3*CH.FrameH/4-Ty))

		Tx = self.TArrTextpos.centerx
		Ty = self.TArrTextpos.centery
		self.screen.blit(self.TArrTime,(3*CH.FrameW/4-Tx,3*CH.FrameH/4-Ty))

		#train timeleft text
		self.TimeLeft = self.FONT.render("In " + NextTrain[2] + " min", 1, (255, 255, 255))
		self.TimeLeftpos = self.TimeLeft.get_rect()
		Tx = self.TimeLeftpos.centerx
		Ty = self.TimeLeftpos.centery
		self.screen.blit(self.TimeLeft,(CH.FrameW/2-Tx,9*CH.FrameH/10-Ty))

		#trains skipped text
		self.SkipTrainsText = self.FONT.render("Skipped " + str(CH.SkipTrains) + " trains", 1, (80, 80, 80))
		self.SkipTrainsTextpos = self.SkipTrainsText.get_rect()
		Tx = self.SkipTrainsTextpos.centerx
		Ty = self.SkipTrainsTextpos.centery
		self.screen.blit(self.SkipTrainsText,(CH.FrameW/2-Tx,CH.FrameH-Ty*2))



		pygame.display.flip()	


	def Stop(self):
		pygame.quit()



if __name__ == '__main__':
	HID = HIDvisuals()
	VR2 = VozniRed2()

	HID.Init()


	SkipTrains = 0
	ESC = False
	while(1):
		NextTrain = VR2.GetTrainTime(CH.TrainStart, CH.TrainStop, CH.SkipTrains)

		HID.Frame(NextTrain)

		#at the end of for() it will refresh 
		for i in range(0,50):
			Key = HID.UserActions()

			if Key == K_ESCAPE:
				ESC = True
				break

			#if key r is pressed or one pinute has passed
			if Key == K_r:
				HID.Frame(("...", "...", "..."))
				break

			if Key == K_RIGHT:
				HID.Frame(("...", "...", "..."))
				CH.SkipTrains += 1
				break

			if Key == K_LEFT:
				HID.Frame(("...", "...", "..."))
				if(CH.SkipTrains>=1):
					CH.SkipTrains -= 1
				break

			
			time.sleep(0.1)

		if(ESC):
			break

			
			

	HID.Stop()