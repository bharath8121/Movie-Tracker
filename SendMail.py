'''
This is your optional module which you wanna use if you want email notifications.
This is important if you are outside and your program is running at your home or office or anywhere.

As you can get email notifications on your smart phone the email acts as communication.

'''

import smtplib, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class SendMail(threading.Thread):
	def __init__(self, username, password, mail_parameters={}):
		threading.Thread.__init__(self)
		self.username = username
		self.password = password
		self.mail_parameters = mail_parameters

	def run(self):
		self._sendMail()

	def _sendMail(self):

		# setting the parameters we want to use.
		subject = self.mail_parameters['subject']
		mail_body = self.mail_parameters['mail_body']
		sendTo = self.mail_parameters['to_addr']
		message = MIMEMultipart()

		# Creating message to send.
		text = MIMEText(mail_body)
		message['subject'] = subject
		message.attach(text)

		# Finding the mail server.
		mail_server = self.username.split('@')[-1]
		print mail_server
		to_request = 'smtp.'+ mail_server +':587'

		# Sending the mail.
		server = smtplib.SMTP(to_request)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(self.username, self.password)
		print "Logged In"
		server.sendmail(self.username, sendTo, message.as_string())
		server.quit()
		print "message sent"
