from pymongo import MongoClient


def main():
	day = "2016-12-12"

	try:
		client = MongoClient('localhost', 27017)
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to server: %s" % e
	db = client.experiments
	tweets = db.tweets.find({"site":"twitter.com", "date":{"$regex": day}}, { "text": 1, "date": 1}).limit(10)

	for tweet in tweets:
		 print(tweet['text'][:10])
		# print("+ "+tweet_date)
		# tweet_text = tweet['text']
        # print("+ "+tweet_text)

#		condition = len(tweet_text) > 0 and len(tweet_text) < 255
#		condition = condition and tweet_text is not None
#		condition = condition and str(tweet['date']) == str(day)


	#tweets_number = tweets.count()

	#print(tweet_date)






if __name__ == "__main__":
	main()
