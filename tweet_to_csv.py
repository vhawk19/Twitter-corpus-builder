#creDs : https://gist.github.com/yanofsky/5436496
import tweepy
import csv
import os

#Twitter API credentials

from dotenv import load_dotenv
load_dotenv()

consumer_key	    = os.getenv('CONSUMER_KEY')
consumer_secret 	= os.getenv('CONSUMER_SECRET')
access_token 		= os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')


def check(tweet):
	""" Shortlist tweets. """
	if tweet.text.startswith('RT'): # remove retweet
		return False
	elif tweet.text.startswith('@'): #remove tweet reply
		return False
	else:
		return True

def formatted(text):
	""" Format the text here. Remove all unwanted chars here."""
	return text.replace('\n', ' ')

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, formatted(tweet.text), tweet.favorite_count]  for tweet in alltweets if check(tweet)]
	# import ipdb; ipdb.set_trace()
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "fav"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("Aash_here_")