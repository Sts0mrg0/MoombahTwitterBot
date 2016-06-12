#!/usr/bin/python
from TwitterFollowBot import TwitterBot
from apscheduler.schedulers.background import BackgroundScheduler
import time

#Bot Config
autoFavPhrasesFile = "autoFavPhrases.txt"
autoRetweetPhrasesFile = "autoRetweetPhrases.txt"
autoFollowPhrasesFile = "autoFollowPhrases.txt"
fetchIntervalMinutes='60'

#Globals
autoFavPhrases = open(autoFavPhrasesFile).readlines()
autoFollowPhrases = open(autoFollowPhrasesFile).readlines()
autoRetweetPhrases = open(autoRetweetPhrasesFile).readlines()

def fetch(bot):
	#actions
	autoRetweet(bot)
	bot.auto_follow_followers()
	autoFollow(bot)
	autoFav(bot)

def autoFollow(bot):
	for phrase in autoFollowPhrases:
		bot.auto_follow(phrase, count=1)

def autoFav(bot):
	for phrase in autoFavPhrases:
		bot.auto_fav(phrase, count=300)

def autoRetweet(bot):
	for phrase in autoRetweetPhrases:
		bot.auto_rt(phrase, count=1)
if __name__ == "__main__":
	print "Starting MoombahBot..."
	
	#init scheduler
	sched = BackgroundScheduler()

	#init bot
	moombahBot = TwitterBot("apiConfig.conf")
	moombahBot.sync_follows()
	fetch(moombahBot)

	#Sync once daily @ 1 AM
	sched.add_job(lambda: moombahBot.sync_follows(), 'cron', hour='1', replace_existing=True)

	#Fetch at interval
	sched.add_job(lambda: fetch(moombahBot), 'cron', minute=fetchIntervalMinutes, replace_existing=True)

	#Run until exit
	print "Moombah Bot Running"
	print "CTRL+C to exit"
	while True:
		time.sleep(1)
