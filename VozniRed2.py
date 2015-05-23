import urllib2
import feedparser
import sys
import time
from Changables import * 
import os
import string



class VozniRed2:
	global CH 
	CH = Changables()

	def GetTrainTimesFromServer(self, start, stop,):
		TrainTimes = [[0 for x in range(2)] for x in range(100)]


		#Razdelitev dvojnih besed
		start = list(start)
		stop = list(stop)

		for i in range (0,len(start)):
			if(start[i] == "-"):
				start[i] = " "

		for i in range (0,len(stop)):
			if(stop[i] == "-"):
				stop[i] = " "

		start = ''.join(start)
		stop = ''.join(stop)

		#get NOW info
		Time = time.localtime(time.time())
		NowHour = Time.tm_hour
		NowMinute = Time.tm_min
		NowDay = Time.tm_mday
		NowMonth = Time.tm_mon
		NowYear = Time.tm_year

		Datum = str(NowDay)+'.'+str(NowMonth)+'.'+str(NowYear)


		#get train data
		response = urllib2.urlopen("http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi")
		page_source = response.read()
		postaje= page_source[page_source.find('44652" >Ajdo'):page_source.find('irovnica')+8]
		vstopna_postaja = postaje[postaje.find(start)-8:postaje.find(start)-3]
		iztopna_postaja = postaje[postaje.find(stop)-8:postaje.find(stop)-3]

		response = urllib2.urlopen('http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi/vozni-red-s-cenikom?entrystation='+vstopna_postaja+'&via=-1&exitstation='+iztopna_postaja+'&date='+Datum)
		page_source = response.read()
		page = page_source[page_source.find(start + " - " + stop):page_source.find('Vozni red velja od')]
		tt = page.split("tr")

		print tt
		 
		#save all times into list
		TrainCount = 0
		
		for i in range(0,len(tt)):
			vrstica = tt[i]
			cas0 = vrstica.find('"time"')
			cas = vrstica.find('"time"',cas0+7)
			if vrstica[cas0+7:cas0+9].isdigit():
				Departure = time.strptime(vrstica[cas0+7:cas0+12], "%H:%M")
				Arrival = time.strptime(vrstica[cas+7:cas+12], "%H:%M")

				TrainTimes[TrainCount][0] = str(Departure.tm_hour).zfill(2)+':'+str(Departure.tm_min).zfill(2)
				TrainTimes[TrainCount][1] = str(Arrival.tm_hour).zfill(2)+':'+ str(Arrival.tm_min).zfill(2)

				TrainCount +=1

		print TrainTimes




	def GetTrainTime(self, start, stop, NumTFromNow):
		TrainTimes = [[0 for x in range(2)] for x in range(100)]


		#Razdelitev dvojnih besed
		start = list(start)
		stop = list(stop)

		for i in range (0,len(start)):
			if(start[i] == "-"):
				start[i] = " "

		for i in range (0,len(stop)):
			if(stop[i] == "-"):
				stop[i] = " "

		start = ''.join(start)
		stop = ''.join(stop)

	
		#get NOW info
		Time = time.localtime(time.time())
		NowHour = Time.tm_hour
		NowMinute = Time.tm_min
		NowDay = Time.tm_mday
		NowMonth = Time.tm_mon
		NowYear = Time.tm_year

		Datum = str(NowDay)+'.'+str(NowMonth)+'.'+str(NowYear)


		#get train data
		response = urllib2.urlopen("http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi")
		page_source = response.read()
		postaje= page_source[page_source.find('44652" >Ajdo'):page_source.find('irovnica')+8]
		vstopna_postaja = postaje[postaje.find(start)-8:postaje.find(start)-3]
		iztopna_postaja = postaje[postaje.find(stop)-8:postaje.find(stop)-3]

		response = urllib2.urlopen('http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi/vozni-red-s-cenikom?entrystation='+vstopna_postaja+'&via=-1&exitstation='+iztopna_postaja+'&date='+Datum)
		page_source = response.read()
		page = page_source[page_source.find(start + " - " + stop):page_source.find('Vozni red velja od')]
		tt = page.split("tr")

		 
		#save all times into list
		NextTrainCount = 0
		
		for i in range(0,len(tt)):
			vrstica = tt[i]
			cas0 = vrstica.find('"time"')
			cas = vrstica.find('"time"',cas0+7)
			if vrstica[cas0+7:cas0+9].isdigit():
				Departure = time.strptime(vrstica[cas0+7:cas0+12], "%H:%M")
				Arrival = time.strptime(vrstica[cas+7:cas+12], "%H:%M")

				if(NowHour<=Departure.tm_hour and NowMinute<Departure.tm_min):

					if(NextTrainCount==NumTFromNow):
						NextDeparture = str(Departure.tm_hour).zfill(2)+':'+str(Departure.tm_min).zfill(2)
						NextArrival = str(Arrival.tm_hour).zfill(2)+':'+ str(Arrival.tm_min).zfill(2)

						TimeLeft = 60*(Departure.tm_hour-NowHour)+Departure.tm_min-NowMinute


						return NextDeparture,NextArrival, str(TimeLeft)

					NextTrainCount +=1


		return "0","0","0"
						

	def GetBusTime(self, Station, BusDir, BusNum):
		#Get data from internet
		Command = os.popen("curl -iH 'Accept: application/json' http://www.trola.si/"+ Station)
		MSG = Command.read()
		Command.close()

		print MSG
		#parse MSG

		#find BusStation in MSG
		TMP =  self.WordInString(Station , MSG)
		if(TMP != 0):
			#find Direction of bus in MSG
			TMP = self.WordInString(BusDir, MSG,TMP)
			if(TMP):
				#find BusNum in MSG
				TMP = self.WordInString(str(BusNum), MSG, TMP)
				if(TMP):
					TMP = self.WordInString('arrivals": [', MSG, TMP)
					if(TMP):
						TMP2 = self.WordInString(']', MSG, TMP)
						if(TMP2):
							return "In " + MSG[TMP+1:TMP2] + " min"


			else:
				print MSG
				print " "
				return "No Direction found with that name. Look for it in this output and copy it to Changables.py"

			return "Data valid"
		else:
			return "No station found with that name"

		return "Error"
				


	def WordInString(self, Word, String, StartLetterNum = 0, NumOfLettersCheck = 0):
		"""lib which finds a word in a string. It returns a)number of last letter of word, if word is found, b)0 if word not found.
			#lib takes in as arguments:
				- Word: word you are looking for (string type)
				- String: string you are looking the Word in (string type)
				- StartLetterNum: The number of letter in String from where on you want to search the Word from
				- NumOfLettersCheck: Number of letters in String you want to include in your search. It takes all as default
		"""
		#set number of letters in String which you are going to check. Default = all
		NOLC = len(String)
		if(NumOfLettersCheck):
			NOLC = NumOfLettersCheck + StartLetterNum
			
		#start parsing
		for i in range(StartLetterNum, NOLC):
			LCount = 0
			for j in range(0,len(Word)):
				if(String[i+j] == Word[j]):
					LCount +=1
					if(LCount == len(Word)):
						return i+j
				else:
					LCount = 0
					break

		return 0

if __name__ == '__main__':
	VR2 = VozniRed2()
	print VR2.GetBusTime(CH.BusStation, CH.BusDirection, CH.BusNum)



		


