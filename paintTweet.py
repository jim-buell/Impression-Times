# Impressions of the Times Twitter Bot

import tweepy
import os
import time
import twitterKeys

# code to get external files
def get_path(filename):
	return os.path.realpath(filename)

# checks time when starting program to make sure we don't spam twitter too often accidentally
def checkTime():
	timeFile = get_path("data/elapsedTime.txt")
	f = open(timeFile, "r", encoding="utf-8")
	lastTime = int(f.read().rstrip())
	currentTime = round(time.time() * 1000)
	elapsedTime = (currentTime - lastTime)
	print("Elapsed time is", round((elapsedTime / 60000)), "minutes.")
	if elapsedTime <= 300000:
		print("Exiting so we don't spam Twitter.")
		exit()

def tweet(tweetText, image):
    
    checkTime()
    twitter_auth_keys = {
        "consumer_key"        : twitterKeys.consumer_key,
        "consumer_secret"     : twitterKeys.consumer_secret,
        "access_token"        : twitterKeys.access_token,
        "access_token_secret" : twitterKeys.access_token_secret
    }
 
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
 
    # Upload image
    media = api.media_upload(image)

	# checks to see if tweet is too long for twitter
    # cuts of headline at first period. Otherwise truncats with "..."
    if len(tweetText) >= 255:
        print("Tweet is", len(tweetText), "characters. The limit is 280 characters.")
        try:
            tweetTemp = tweetText.split(".", 1)
            tweetText = tweetTemp[0]
            if len(tweetText) >= 255:
                tweetText = (tweetText[:252] + "...")
            print("Splitting the headline. It's super long.")
        except:
            tweetText = (tweetText[:252] + "...")
            print("Error occured. Maybe there wasn't a period to split the text at.")

    # tweets new headlines
    # Post tweet with image
    post_result = api.update_status(status = tweetText, media_ids = [media.media_id])

    # print tweet to terminal
    print("Tweet is", len(tweetText), "characters. Tweeting:")
    print(tweetText)

	# record time of headline fetch in milliseconds from epoch
    timeFile = get_path("data/elapsedTime.txt")
    currentTime = round(time.time() * 1000)
    f = open(timeFile, "w", encoding="utf-8")
    timeStr = str(currentTime)
    f.write(timeStr)
    f.close()
	
# Main loop and scheduled functions
# ————————————————————————————————————————————————————————————————————————————————————————————————————
