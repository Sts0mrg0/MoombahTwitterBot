#!/usr/bin/python
from TwitterFollowBot import TwitterBot
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
import sys

#Bot Config
autoFavPhrasesFile = "autoFavPhrases.txt"
autoRetweetPhrasesFile = "autoRetweetPhrases.txt"
autoFollowPhrasesFile = "autoFollowPhrases.txt"
fetchIntervalMinutes = 60
logfile = "log.txt"

#Globals
autoFavPhrases = open(autoFavPhrasesFile).readlines()
autoFollowPhrases = open(autoFollowPhrasesFile).readlines()
autoRetweetPhrases = open(autoRetweetPhrasesFile).readlines()

#Init Logger
sys.stdout = open(logfile, 'w')
logger = logging.getLogger('MoombahBot')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def fetch(bot):
	#actions
	logger.info('[+]Fetching...')
	autoRetweet(bot)
	bot.auto_follow_followers()
	autoFollow(bot)
	autoFav(bot)

def autoFollow(bot):
	logger.info('[-]Starting autoFollow')
	for phrase in autoFollowPhrases:
		try:
			bot.auto_follow(phrase, logger=logger, count=1)
		except Exception as e:
			logger.error(e)

def autoFav(bot):
	logger.info('[-]Starting autoFavorite')
	for phrase in autoFavPhrases:
		try:
			bot.auto_fav(phrase, logger=logger, count=300)
		except Exception as e:
			logger.error(e)

def autoRetweet(bot):
	logger.info('[-]Starting autoRetweet')
	for phrase in autoRetweetPhrases:
		try:
			bot.auto_rt(phrase, logger=logger, count=1)
		except Exception as e:
			logger.error(e)

if __name__ == "__main__":
	#start
	logger.info("[+]Starting MoombahBot")
	
	#init scheduler
	sched = BackgroundScheduler()

	#init bot
	moombahBot = TwitterBot("apiConfig.conf")

	#Sync once daily
	sched.add_job(lambda: moombahBot.sync_follows(), 'interval', hours=23, replace_existing=True)
	logger.debug('Account sync cronjob added: every 23 hours')

	#Fetch at interval
	sched.add_job(lambda: fetch(moombahBot), 'interval', minutes=fetchIntervalMinutes, replace_existing=True)
	logger.debug('Fetch cronjob added: every', str(fetchIntervalMinutes), 'minutes')

	#Running
	logger.info("[+]Moombah Bot Running")
	logger.info("[+]CTRL+C to exit")
	
	#Sync+fetch on start
	#moombahBot.sync_follows()
	fetch(moombahBot)

	while True:
		time.sleep(1)
