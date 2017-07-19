from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import sys, os, subprocess
import pandas as pd
import numpy as np
# same as cd /web/ --> cd ../ --> cd src
lib_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(lib_path)
from sentiment import Sentiment
from calculator import Calculator
from hmm import Hmm

app = Flask(__name__)
mysql = MySQL(app)

#set up mysql options
app.config['MYSQL_HOST'] = '127.0.0.1' # <-- db if docker
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'experiments'


#routes
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/demo', methods=['GET','POST'])
def demo():
	if request.method == 'POST':
		vocabulary = str(request.form['vocabulary'])
		market = str(request.form['market'])
		#standard, variazione, variazione_5

		############# SENTIMENT
		sent  = Sentiment(vocabulary, "tweets", 4) #only vocabulary is important

		############# TRANSITION AND EMISSION MODEL
		#root = "/Users/maca/Desktop/UNIVERSITA/MODELLI/Brexit-marketValue/data/preprocessed_data/output/"
		root = "D:\Dropbox\Git_Projects\Brexit-marketValue\data\preprocessed_data\output\\"
		market_transition_f = root+"output_market_"+vocabulary+"_market_from_"+market+".txt"
		market_emission_f	= root+"output_market_"+vocabulary+"_market_from_"+market+".txt"
		sentiment_f = root+"output_sentiment_"+vocabulary+"_market_from_"+market+".txt"

		calc = Calculator(market_transition_f, market_emission_f, sentiment_f)

		emission_mod = str(request.form['emission_mod'])
		transition_mod = str(request.form['transition_mod'])
		market_tollerance = float(request.form['market_tollerance'])
		sentiment_tollerance = float(request.form['sentiment_tollerance'])

		# if market dataset is different for transition and emission
		if transition_mod == "variazione":
			hiddenVars = calc.col_select(calc.delta(calc.market_transition_f, market_tollerance), 2)
			hiddenVars_labels = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]]

		elif transition_mod == "variazione_5":
			hiddenVars = calc.col_select(calc.delta(calc.market_transition_f, market_tollerance), 5)
			hiddenVars_labels = [["saleTanto", "saleTanto"], ["salePoco", "salePoco"], ["stabile", "stabile"], ["scendePoco", "scendePoco"], ["scendeTanto", "scendeTanto"]]

		calc.build_transition_m(hiddenVars, hiddenVars_labels)

		if emission_mod == "standard":
			observations = calc.col_select( calc.delta( calc.sentiment_f, sentiment_tollerance), 4)
			observations_labels = [["sent+", "pos"], ["sent-", "neg"]]

		elif emission_mod == "variazione":
			observations = calc.col_select( calc.delta( calc.sentiment_f, sentiment_tollerance), 2)
			observations_labels = [["sentSale", "sale"], ["sentStabile", "stabile"], ["sentScende", "scende"]]

		elif emission_mod == "variazione_5":
			observations = calc.col_select(calc.delta( calc.sentiment_f, sentiment_tollerance), 5)
			observations_labels = [["sentSaleTanto", "saleTanto"], ["sentSalePoco", "salePoco"], ["sentStabile", "stabile"], ["sentScendePoco", "scendePoco"], ["sentScendeTanto", "scendeTanto"]]

		calc.build_emission_m(hiddenVars, observations, hiddenVars_labels, observations_labels)


		I = []
		if transition_mod == "variazione":
			I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
		elif transition_mod == "variazione_5":
			I = [0.2, 0.2, 0.2, 0.2, 0.2]

		hmm_model = Hmm(I, calc.T, calc.O)
		steps = observations.__len__()

		filtering_result = hmm_model.filtering(steps, observations, observations_labels, hiddenVars_labels)
		filtering_seq = hmm_model.get_steps()
		print("\nFITERING: ")
		correspondence_filtering = correspondence(hiddenVars, hmm_model.get_steps())

		#steps = 97
		#hmm_model.prediction(steps, observations[:90], observations_labels, hiddenVars_labels)

		print("\nVITERBI:")
		del observations[0]  # delete first element: "nullo"
		viterbi_seq = hmm_model.viterbi(observations, observations_labels, hiddenVars_labels)
		correspondence_viterbi = correspondence(hiddenVars, viterbi_seq)

		prob_matrix = np.round(I, 3)
		transition_matrix = np.round(calc.T, 3)
		emission_matrix = np.round(calc.O, 3)

		# LABELS ALL STEPS
		# 0			  1					2		3			4
		# prediction_step | prediction_Step_label | update | normalization | normalization label
		all_steps = hmm_model.steps
		emission_matrix_len=np.array(emission_matrix).transpose().__len__()
		data = True
		return render_template('demo.html', prob_matrix=prob_matrix, transition_matrix= transition_matrix, emission_matrix=emission_matrix,
						 prob_matrix_len=len(I), transition_matrix_len=len(calc.T),emission_matrix_len=emission_matrix_len,
						 viterbi_seq = viterbi_seq, filtering_seq = filtering_seq,
						 filtering_result = filtering_result, steps = steps,
						 correspondence_filtering=correspondence_filtering, correspondence_viterbi=correspondence_viterbi,
						 all_steps = all_steps, data=data)
	else:
		return render_template('demo.html')

#sentiment
@app.route('/sentiment', methods=['POST', 'GET'])
def sentiment():
	if request.method == 'POST':
		tweet = str(request.form['tweet'])
		dictionary = str(request.form['dictionary'])
		#calculate sentiment
		sentiment_main = Sentiment(dictionary, "", 0)
		sentiment = sentiment_main.sentiment(tweet)
		#check if sentiment is zero
		if sentiment == 0.0:
			sentiment = "zero. No words found."

		return render_template('sentiment.html', tweet=tweet, dictionary=dictionary, sentiment=sentiment)
	else:
		return render_template('sentiment.html')

#correlation
@app.route('/correlation', methods=['POST', 'GET'])
def correlation():
		return render_template('correlation.html')

@app.route('/load/graph', methods=['POST', 'GET'])
def data():
	data=[]
	print(str(request.json))
	vocabulary = str(request.args.get('vocabulary'))
	market = str(request.args.get('market'))
	#root = "/Users/maca/Desktop/UNIVERSITA/MODELLI/Brexit-marketValue/data/preprocessed_data/gui_files/"
	# root = "../data/preprocessed_data/gui_files/"
	root = "D:\Dropbox\Git_Projects\Brexit-marketValue\data\preprocessed_data\gui_files\\"

	market_f = root+"marketVariation_"+market+".txt"

	file = open(market_f)

	days_temp = []
	column1=[]
	column2=[]
	column3=[]
	for line in file:
		splitted_line = line.split("\t")
		column1.append(splitted_line[0])
		column2.append(splitted_line[1][:-1])
	file.close()


	sentiment_f = root+"sentimentVariation_"+vocabulary+"_"+market+".txt"

	file = open(sentiment_f)

	for line in file:
		splitted_line = line.split("\t")
		column3.append(splitted_line[1][:-1])
	file.close()
	data.append(column1)

	data.append(normalize(column2))

	data.append(normalize(column3))

	return jsonify(data)

#tweets
@app.route('/tweets')
@app.route('/tweets/<name>/<offset>/<limit>')
def tweets(offset=0,limit=10,name="tweets"):
	if int(offset) < 0:
		offset = 0
	if int(limit) < 0:
		limit=10

	cur = mysql.connection.cursor()
	cur.execute("SELECT id_tweet, tweet, tweet_date  FROM "+name+" LIMIT "+str(offset)+", "+str(limit))
	result = cur.fetchall()
	data = {}
	for row in result:
		data[str(row[0])] = (row[1],row[2])

	return render_template('tweets.html',data=data, name=name, offset=offset, limit=limit)


# dictionaries
@app.route('/dictionary')
@app.route('/dictionary/<name>/<offset>/<limit>')
def dictionary(offset=0,limit=10,name="bing"):
	if int(offset) < 0:
		offset = 0
	if int(limit) < 0:
		limit=10

	cur = mysql.connection.cursor()
	cur.execute("SELECT word, label FROM "+name+" LIMIT "+str(offset)+", "+str(limit))
	result = cur.fetchall()
	data = {}
	for row in result:
		data[str(row[0])] = row[1]

	return render_template('dictionary.html',data=data, name=name, offset=offset, limit=limit)

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


def correspondence(state, prediction):
	count_corr = 0.0
	for count in range(1, state.__len__()):
		if str(state[count]) == str(prediction[count - 1]):
			count_corr += 1

	print "STATE"
	print "[",
	for i in range(0, state.__len__()):
		print( str(state[i]) +" "),
	print  "]"

	print "PREDICTION"
	print(prediction)

	return str(count_corr / float(state.__len__() - 1))

def normalize(list):
	sum = 0.0
	for el in list:
		sum += float(el)

	alpha = 1.0 / float(sum)
	normalized_list = []
	for el in list:
		normalized_list.append(alpha * float(el))

	return normalized_list


if __name__ == '__main__':
	app.run(host='0.0.0.0')
