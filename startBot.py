#!/usr/bin/python
'''
Author: Hunter Gregal - huntergregal.com - @huntergregal
'''
from TwitterFollowBot import TwitterBot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
import time
import logging
import sys

#Bot Config
apiConfFile = "apiConfig.conf"
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
sys.stdout = open(logfile, 'w+')
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
			logger.error("autoFollow: %s" % repr(e))

def autoFav(bot):
	logger.info('[-]Starting autoFavorite')
	for phrase in autoFavPhrases:
		try:
			bot.auto_fav(phrase, logger=logger, count=300)
		except Exception as e:
			logger.error("autoFav: %s" % repr(e))

def autoRetweet(bot):
	logger.info('[-]Starting autoRetweet')
	for phrase in autoRetweetPhrases:
		try:
			bot.auto_rt(phrase, logger=logger, count=1)
		except Exception as e:
			logger.error("autoRetweet: %s" % repr(e))

def fetchCronListener(event):
	if event.exception:
		logger.error("FetchCronListener: %s" % repr(event.exception))
	else:
		logger.info("Fetching Complete w/ no errors!")

def syncCronListener(event):
	if event.exception:
		logger.error("syncCronListener: %s" % repr(event.exception))
	else:
		logger.info("Syncing Complete w/ no errors!")
if __name__ == "__main__":
	#start
	logger.info("[+]Starting MoombahBot")
	
	#init scheduler
	sched = BackgroundScheduler()

	#init bot
	moombahBot = TwitterBot(config_file=apiConfFile, logger=logger)

	#Sync once daily
	sched.add_job(lambda: moombahBot.sync_follows(), 'interval', hours=23, replace_existing=True)
	sched.add_listener(fetchCronListener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
	logger.debug('Account sync cronjob added')

	#Fetch at interval
	sched.add_job(lambda: fetch(moombahBot), 'interval', minutes=fetchIntervalMinutes, replace_existing=True)
	sched.add_listener(syncCronListener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
	logger.debug('Fetch cronjob added')
	
	#start sched cron
	sched.start()

	#Running
	logger.info("[+]Moombah Bot Running")
	print("[+]CTRL+C to exit or ps aux|grep startBot.py")
	
	#Sync+fetch on start
	try:
		logger.info("[+]Starting initial sync...")
		moombahBot.sync_follows()
		logger.info("[+]Initial sync complete")
	except Exception as e:
		logger.error("Initial sync: %s" % repr(e))
	try:	
		logger.info("[+]Starting initial fetch...")
		fetch(moombahBot)
		logger.info("[+]Initial fetch complete")
	except Exception as e:
		logger.error("Initial fetch: %s" % repr(e))

	#Run as background thread
	while True:
		time.sleep(1)

