import urllib2
import feedparser
import sys


start = sys.argv[1]
stop = sys.argv[2]

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



response = urllib2.urlopen("http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi")
page_source = response.read()
postaje= page_source[page_source.find('44652" >Ajdo'):page_source.find('irovnica')+8]
vstopna_postaja = postaje[postaje.find(start)-8:postaje.find(start)-3]
iztopna_postaja = postaje[postaje.find(stop)-8:postaje.find(stop)-3]

response = urllib2.urlopen('http://www.slo-zeleznice.si/sl/potniki/slovenija/vozni-redi/vozni-red-s-cenikom?entrystation='+vstopna_postaja+'&via=-1&exitstation='+iztopna_postaja+'&date=13.5.2015')
page_source = response.read()
page = page_source[page_source.find(start + " - " + stop):page_source.find('Vozni red velja od')]
tt = page.split("tr")




for i in range(0,len(tt)):
	vrstica = tt[i]
    cas0 = vrstica.find('"time"')
    cas = vrstica.find('"time"',cas0+7)
    if vrstica[cas0+7:cas0+9].isdigit():
        print start + " " + vrstica[cas0+7:cas0+12] + "  " + stop + " " + vrstica[cas+7:cas+12]

#d = feedparser.parse('http://ice.slo-zeleznice.si/cool-ice/default.asp?Category=E-zeleznice&Service=Zamude_RSS')
#for x in range (1,len(d['entries'])):
#    print d.entries[x].summary
#    print "....................."