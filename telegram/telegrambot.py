import sys, time, os
import telepot
import speech_recognition as sr
import smtplib


TELEGRAM_API = 'XXX'
GM_USERNAME = 'XXX'
GM_PASSWORD = 'XXX'
MAIL_TO  = 'XXX'
TELEGRAM_ID = XXX
GOOGLE_SPEECH_KEY = "XXX"


def dateStringFromTimestamp(t):
	return str(time.strftime("%Y%m%d%H%M%S", time.localtime(float(t))))

class MementoBot(object):
	def __init__(self):
		global TELEGRAM_API
		self.state = ''
		self.bot = telepot.Bot(TELEGRAM_API)
		self.bot.notifyOnMessage(self.handle)

	def sendmail(self, subject, content):
		global GM_USERNAME
		global GM_PASSWORD
		global MAIL_TO
		fromaddr = GM_USERNAME + '@gmail.com'
		message = "\r\n".join([
		"From: " + fromaddr,
		"To: " + MAIL_TO,
		"Subject: " + subject,
		"",
		content
		])
		server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
		server_ssl.login(GM_USERNAME, GM_PASSWORD)  
		server_ssl.sendmail(fromaddr, MAIL_TO, message)
		server_ssl.quit()
		server_ssl.close()
		global TELEGRAM_ID
		self.bot.sendMessage(TELEGRAM_ID, 'successfully sent mail')

	def handle_audio(self, message):
		d = dateStringFromTimestamp(message['date'])
		r = sr.Recognizer()
		file_path = d + '_voice.ogg'
		self.bot.downloadFile(message['voice']['file_id'], file_path)
		os.system('ffmpeg -y -i ' + file_path + ' audio.wav')
		with sr.WavFile("audio.wav") as source:
			audio = r.record(source)
		try:
			transcription = r.recognize_google(audio, language="en-US", key=GOOGLE_SPEECH_KEY)
			print("Transcription: " + transcription)
			self.sendmail("recuerda", transcription)
		except LookupError:
			print("Could not understand audio")

	def handle_photo(self, message):
		fv = message['photo'][-1]
		for fvi in message['photo']:
			if int(fvi['file_size']) > int(fv['file_size']):
				fv = fvi
		self.bot.downloadFile(fv['file_id'], d+'_photo.png')

	def handle_video(self, message):
		self.bot.downloadFile(message['video']['file_id'], d+'_video.mpg')


	def handle_document(self, message):
		self.bot.downloadFile(message['document']['file_id'], d+'_document.file')

	def handle_text(self, message):
		print 'text: ', message['text']
		self.sendmail("recuerda", message['text'])

	def handle(self, message):
		print message
		if 'text' in message.keys():
			self.handle_text(message)
		elif 'voice' in message.keys():
			self.handle_audio(message)
		elif 'photo' in message.keys():
			self.handle_photo(message)
		elif 'video' in message.keys():
			self.handle_video(message)
		elif 'document' in message.keys():
			self.handle_document(message)
		else:
			print message

eebot = MementoBot()
while 1:
    time.sleep(10)


