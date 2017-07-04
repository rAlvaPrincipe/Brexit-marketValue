import MySQLdb
import math
import copy

class Sentiment:
	vocabulary = {}
	tweet_table = ""
	days = []
	output_f = ""

	def __init__(self, vocabulary_name, tweet_table, weeks ):
		self.retrieve_vocabulary(vocabulary_name)
		self.tweet_table = tweet_table
		self.output_f =  "w" + str(weeks) + "_" + vocabulary_name + "_" + tweet_table + ".txt"
		if weeks == 4:
			self.days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
						 '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
						 '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
						 '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']
		elif weeks == 5:
			self.days = ['2016/11/28', '2016/11/29', '2016/11/30', '2016/12/01', '2016/12/02',
						 '2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
						 '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
						 '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
						 '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30',
						 '2017/01/02', '2017/01/03', '2017/01/04', '2017/01/05', '2017/01/06']


	## returns the database vocabulary as python dictionary
	## input: vocabulary_request = "bing"
	## output: {'love': +2, 'hate': -2, 'abacus': 0, ...}
	def retrieve_vocabulary(self, vocabulary_request):
		vocabulary2={}
		db = MySQLdb.connect(host="127.0.0.1",
							 user="root",
							 passwd="root",
							 db="experiments")

		# Create and execute SQL query
		cursor = db.cursor()
		query = "SELECT * FROM " +  vocabulary_request + ";"
		try:
			cursor.execute(query)
			print(query)
			results = cursor.fetchall()
			# add 'word':'label' in vocabulary for every word in database
			for row in results:
				w = row[0]
				l = int(row[1])
				vocabulary2[w] = l

		except:
			print("Error dictionary: unable to fetch data.")

		db.close()
		self.vocabulary = vocabulary2




	## day_sentiment(day) returns the sentimant of the day according to vocab
	## input: day = "2016/12/05"
	##		vocab = {'love': +2, 'hate': -2, 'abacus': 0, ... }
	## output: 0.112
	def day_sentiment(self, day):
		pos_daySentiment = 0.0
		neg_daySentiment = 0.0

		db = MySQLdb.connect(host="127.0.0.1",
							user="root",
							passwd="root",
							db="experiments")

		# Create and execute SQL query
		cursor = db.cursor()
		query = "SELECT tweet FROM "+ self.tweet_table +" WHERE tweet_date = \'" + day + "\';"
		try:
			cursor.execute(query)
			print(query)
			results = cursor.fetchall()
			for row in results:
				tweet = str(row[0])
				score = self.sentiment(tweet)  # sentiment of single tweet
				if score > 0:
					pos_daySentiment += 1
				elif score < 0:
					neg_daySentiment+= 1
		except:
			print("Error tweets: unable to fetch data.")
		db.close()

		# calculate sentiment with simple sentiment logit scale sentiment formula
		daySentiment = (1 + pos_daySentiment) / (1 + neg_daySentiment)
		
		return math.log(daySentiment)



	## returns the sentiment of the tweet according to vocab
	## input: tweet = "love love love hate #xyz" 
	##		vocab = {'love': +2, 'hate': -2, ... }
	## output: 4.0
	def sentiment(self, tweet):
		score = 0.0			
		words = tweet.split(' ' )  #split in words

		#remove non alpha characters
		for i in range (0, words.__len__()):
			words[i] = filter(str.isalpha, words[i])
			if (self.vocabulary.get(words[i]) != None):
				score += int(self.vocabulary.get(words[i]))
		return score


	def generate_observations(self):
		days_sentiment = {}
		out_file = open(self.output_f, "w")
		for i in range(0, self.days.__len__()):
			days_sentiment[i] = self.day_sentiment(self.days[i])
			out_file.write(self.days[i] + "\t" + str(days_sentiment[i]) + "\n")
			print(days_sentiment[i])
		out_file.close()


#sent  = Sentiment("afinn111", "tweets", 5)
#sent.generate_observations()
