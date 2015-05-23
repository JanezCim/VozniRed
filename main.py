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

	__slots__ = ['NextTrainText', 'NextBusText']



	def Init(self):
		self.NextTrainText = ["0","0","0"]
		self.NextBusText = "0"

		pygame.init()
		pygame.display.set_caption('IOTGUI')

		self.screen=pygame.display.set_mode((CH.FrameW, CH.FrameH))

		self.FONT = pygame.font.Font(None,CH.TextSize)

		#pic import and transform
		self.BusPic = pygame.image.load('Bus.png')
		self.BusPic = pygame.transform.scale(self.BusPic, (CH.PicWCOF, CH.PicHCOF))
		self.TrainPic = pygame.image.load('Train.png')
		self.TrainPic = pygame.transform.scale(self.TrainPic, (CH.PicWCOF, CH.PicHCOF))



	def UserActions(self):
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
				self.OLDKeyPress = self.ToReturn = event.key
				
			if (event.type == KEYUP):
				if (event.key==self.OLDKeyPress):
					self.ToReturn = 0
		
		return self.ToReturn




	def Frame(self):
		self.screen.fill((0,0,0))

		#position the pictures
		self.screen.blit(self.BusPic,(CH.FrameW/2-CH.PicWCOF/2,CH.FrameH/4-CH.PicHCOF/2))
		self.screen.blit(self.TrainPic,(CH.FrameW/2-CH.PicWCOF/2,3*CH.FrameH/4-CH.PicHCOF/2))

		#stops text render
		TrainStartText = self.FONT.render(CH.TrainStart, 1, (255, 255, 255))
		TStartTextpos = TrainStartText.get_rect()
		TrainStopText = self.FONT.render(CH.TrainStop, 1, (255, 255, 255))
		TStopTextpos = TrainStopText.get_rect()

		# train position stops Text
		Tx = TStartTextpos.centerx
		Ty = TStartTextpos.centery
		self.screen.blit(TrainStartText,(CH.FrameW/4-Tx, 2*CH.FrameH/3-Ty))
		Tx = TStopTextpos.centerx
		Ty = TStopTextpos.centery
		self.screen.blit(TrainStopText,(3*CH.FrameW/4-Tx, 2*CH.FrameH/3-Ty))

		# train text
		TDepTime = self.FONT.render(self.NextTrainText[0], 1, (255, 255, 255))
		TDepTextpos = TDepTime.get_rect()

		TArrTime = self.FONT.render(self.NextTrainText[1], 1, (255, 255, 255))
		TArrTextpos = TArrTime.get_rect()

		Tx =TDepTextpos.centerx
		Ty =TDepTextpos.centery
		self.screen.blit(TDepTime,(CH.FrameW/4-Tx,3*CH.FrameH/4-Ty))

		Tx = TArrTextpos.centerx
		Ty = TArrTextpos.centery
		self.screen.blit(TArrTime,(3*CH.FrameW/4-Tx,3*CH.FrameH/4-Ty))

		#train timeleft text
		TimeLeft = self.FONT.render("In " + self.NextTrainText[2] + " min", 1, (255, 255, 255))
		TimeLeftpos = TimeLeft.get_rect()
		Tx = TimeLeftpos.centerx
		Ty = TimeLeftpos.centery
		self.screen.blit(TimeLeft,(CH.FrameW/2-Tx,9*CH.FrameH/10-Ty))

		#bus stops text render
		BStartText = self.FONT.render(CH.BusStation, 1, (255, 255, 255))
		BStartTextPos = BStartText.get_rect()
		BDirText = self.FONT.render(CH.BusDirection, 1, (255, 255, 255))
		BDirTextPos = BDirText.get_rect()
		BNumText = self.FONT.render(str(CH.BusNum), 1, (255, 255, 255))
		BNumTextPos = BNumText.get_rect()
		DirText1 = self.FONT.render("Start Station:", 1, (255, 255, 255))
		DirText2 = self.FONT.render("Direction:", 1, (255, 255, 255))


		#bus text position
		Tx = BNumTextPos.centerx
		Ty = BNumTextPos.centery
		self.screen.blit(BNumText,(CH.FrameW/2-Tx,Ty*4))

		Tx = BStartTextPos.centerx
		Ty = BStartTextPos.centery
		self.screen.blit(DirText1,(CH.FrameW/4-Tx, CH.FrameH/6-Ty))
		self.screen.blit(BStartText,(CH.FrameW/4-Tx, CH.FrameH/4-Ty))

		Tx = BDirTextPos.centerx
		Ty = BDirTextPos.centery
		self.screen.blit(DirText2,(3*CH.FrameW/4-Tx, CH.FrameH/6-Ty))
		self.screen.blit(BDirText,(3*CH.FrameW/4-Tx, CH.FrameH/4-Ty))


		#Bus time left 
		BTimeLeft = self.FONT.render(self.NextBusText, 1, (255, 255, 255))
		BTimeLeftPos = BTimeLeft.get_rect()
		Tx = BTimeLeftPos.centerx
		Ty = BTimeLeftPos.centery
		self.screen.blit(BTimeLeft,(CH.FrameW/2-Tx, CH.FrameH/2-Ty))


		#trains/buses skipped text
		SkipText = self.FONT.render("Skipped " + str(CH.Skip) + " trains", 1, (80, 80, 80))
		SkipTrainsPos = SkipText.get_rect()
		Tx = SkipTrainsPos.centerx
		Ty = SkipTrainsPos.centery
		self.screen.blit(SkipText,(CH.FrameW/2-Tx,CH.FrameH-Ty*2))


		pygame.display.flip()	


	def Stop(self):
		pygame.quit()



if __name__ == '__main__':
	HID = HIDvisuals()
	VR2 = VozniRed2()

	HID.Init()


	Skip = 0
	ESC = False
	while(1):
		HID.NextTrainText = VR2.GetTrainTime(CH.TrainStart, CH.TrainStop, CH.Skip)
		HID.NextBusText = VR2.GetBusTime(CH.BusStation, CH.BusDirection, CH.BusNum)

		HID.Frame()

		#at the end of for() it will refresh 
		for i in range(0,50):
			Key = HID.UserActions()

			if Key == K_ESCAPE:
				ESC = True
				break

			#if key r is pressed or one pinute has passed
			if Key == K_r:
				HID.NextTrainText = ("...", "...", "...")
				HID.Frame()
				break

			if Key == K_RIGHT:
				HID.NextTrainText = ("...", "...", "...")
				HID.Frame()
				CH.Skip += 1
				break

			if Key == K_LEFT:
				HID.NextTrainText = ("...", "...", "...")
				HID.Frame()
				if(CH.Skip>=1):
					CH.Skip -= 1
				break

			
			time.sleep(0.1)

		if(ESC):
			break

			
			

	HID.Stop()