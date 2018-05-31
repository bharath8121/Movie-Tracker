'''
This is a Movie Tracker which tracks the your favorite movie in your desired theatres
and sends you email and desktop notification. So you cannot miss your movie on the first day.

you need to install the below mentioned modules.

BeautifulSoup
Gtk3
pygame 

'''




import bs4, requests, smtplib, time, threading
from gi import require_version
require_version('Notify', '0.7')
from gi.repository import Notify
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from pygame import mixer
from SendMail import SendMail

class BMSObject:
	def __init__(self, link):
		self.link = link
		self.request = requests.get(self.link)
		if self.request.status_code == 200:
			self.parser = bs4.BeautifulSoup(self.request.text)
		else:
			print "The link is invalid. Please check it again."
		
	# Refreshes the page we want.
	def refresh(self):
		self.request = requests.get(self.link)
		if self.request.status_code == 200:
			self.parser = bs4.BeautifulSoup(self.request.text)
		else:
			print "The link is invalid. Please check it again."

	# Gives the Theatre list.
	def getTheatreList(self):
		theatreList = self.parser.select('div[class="__name "] > a[class="__venue-name"] > strong')
		return map(lambda x: x.getText(), theatreList)

	# Checks whether the Theatre is available.
	def theatreAvailability(self, name):
		return name in self.getTheatreList()

	# Shows available in a Theatre.
	def showsAvailable(self, name):
		selector = 'ul[id="venuelist"] > li[class="list"]'
		showsList = self.parser.select(selector)
		return map(lambda x:x.getText(), showsList)

	# Books tickets on your request.
	def bookTickets(self, seat_preferance):
		pass

	# Check whether tickets are available at given Theatres.
	def trackTheatres(self, names=[]):
		for i in names:
			Tracker(self.link, i).start()



class Tracker(threading.Thread):
	def __init__(self, link, name):
		threading.Thread.__init__(self)
		self.link = link
		self.name = name
		# Give your email here.
		self.username = ''
		# Give your password here.
		self.password = ''

	def run(self):
		print "Starting the track for " + self.name
		trackIt = True
		trackerObject = BMSObject(self.link)
		while trackIt:
			if trackerObject.theatreAvailability(self.name):
				self.throwNotification()
				self.playMixer()
				self.sendMail()
				print "Exiting the track"
				trackIt = False
			else:
				time.sleep(10)
				trackerObject.refresh()

	def throwNotification(self):
		Notify.init("Book My Show Tracker")
		Notify.Notification.new("Tickets at " + self.name + " are open now").show()
		
	def playMixer(self):
		path = "/root/Downloads/mom_alert.mp3"
		mixer.init()
		mixer.music.load(path)
		mixer.music.play()
		time.sleep(3)
		mixer.music.stop()

	# Sends a mail to your mail id.
	def sendMail(self):
		mail_parameters = {'subject': 'Book My Show Tracker',
							'mail_body': 'Tickets at ' + self.name + ' are open now',
							'to_addr': self.username}
		SendMail(self.username, self.password, mail_parameters).start()

def main():
	# Give your movie link down inside the quotes, the link which has the theatre list.
	myObj = BMSObject('')
	# Give your Theatre list here.
	names = ['Asian CineSquare Multiplex: Uppal']
	# This line tracks theatres.
	myObj.trackTheatres(names)

if __name__ == '__main__':
	main()