import urllib2
import feedparser
import sys
import time



class VozniRed2:

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
						


