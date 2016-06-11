#!/usr/bin/python
from TwitterFollowBot import TwitterBot
from apscheduler.schedulers.background import BackgroundScheduler
import time

#Bot Config
autoFavPhrasesFile = "autoFavPhrases.txt"
autoRetweetPhrasesFile = "autoRetweetPhrases.txt"
fetchIntervalMinutes='30'

#Globals
autoFavPhrases = open(autoFavPhrasesFile).readlines()

def fetch(bot):
	#actions
	autoFav(bot)
	bot.auto_follow_followers()
	bot.auto_follow_followers_of_user("MoombahSC", count=1000)

def autoFav(bot):
	for phrase in autoFavPhrases:
		moombahBot.auto_fav(phrase, count=1000)
		
if __name__ == "__main__":
	print "Starting MoombahBot..."
	
	#init scheduler
	sched = BackgroundScheduler()

	#init bot
	moombahBot = TwitterBot("apiConfig.conf")
	moombahBot.sync_follows()
	fetch(moombahBot)

	#Sync once daily @ 1 AM
	sched.add_job(lambda: moombahBot.sync_follows(), 'cron', hour='1')

	#Fetch at interval
	sched.add_job(lambda: fetch(moombahBot), 'cron', minute=fetchIntervalMinutes)

	#Run until exit
	print "Moombah Bot Running"
	print "CTRL+C to exit"
	while True:
		time.sleep(1)
