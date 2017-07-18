import pandas as pd
import numpy as np
from sentiment import Sentiment
from calculator import Calculator
from hmm import Hmm

class Interface:
	def correspondence(self, state, prediction):
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



	def compute(self, vocabulary, transition_discretization, sentiment_discretization, input_emission_mod, market_tollerance, sentiment_tollerance):

	 #========================================================== SENTIMENT =========================================================================


		dataset_tweets = "tweets"
		n_weeks = 4
		sent  = Sentiment(str(vocabulary), dataset_tweets, n_weeks)
	#	sent.generate_observations()


	 #===================================================TRANSITION AND EMISSION MODEL =============================================================

		market_transition_f = "../data/preprocessed_data/output/output_market_afinn_bing_base_afinn_market_from_ecb.europa.eu.txt"
		market_emission_f   = "../data/preprocessed_data/output/output_market_afinn_bing_base_afinn_market_from_ecb.europa.eu.txt"
		market_emission_f = market_transition_f
		calc = Calculator(market_transition_f, market_emission_f, sent.output_f)

		I = []
		hiddenVars =""
		hiddenVars_labels = ""
	 	observations=""
		observations_labels = ""
		if transition_discretization == 3:
			hiddenVars = calc.col_select(calc.delta(calc.market_transition_f, market_tollerance), 2)
			hiddenVars_labels = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]]
			I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]


		elif transition_discretization == 5:
			hiddenVars = calc.col_select(calc.delta(calc.market_transition_f, market_tollerance), 5)
			hiddenVars_labels = [["saleTanto", "saleTanto"], ["salePoco", "salePoco"], ["stabile", "stabile"], ["scendePoco", "scendePoco"], ["scendeTanto", "scendeTanto"]]
			I = [0.2, 0.2, 0.2, 0.2, 0.2]

		calc.build_transition_m(hiddenVars, hiddenVars_labels)





		if sentiment_discretization == 2:
			observations = calc.col_select( calc.delta( calc.sentiment_f, sentiment_tollerance), 4)
			observations_labels = [["sent+", "pos"], ["sent-", "neg"]]

		elif sentiment_discretization == 3:
			observations = calc.col_select( calc.delta( calc.sentiment_f, sentiment_tollerance), 2)
			observations_labels = [["sentSale", "sale"], ["sentStabile", "stabile"], ["sentScende", "scende"]]

		elif sentiment_discretization == 5:
			observations = calc.col_select(calc.delta( calc.sentiment_f, sentiment_tollerance), 5)
			observations_labels = [["sentSaleTanto", "saleTanto"], ["sentSalePoco", "salePoco"], ["sentStabile", "stabile"], ["sentScendePoco", "scendePoco"], ["sentScendeTanto", "scendeTanto"]]



		calc.build_emission_m(hiddenVars, observations, hiddenVars_labels, observations_labels)

		result = []  # matrici
		result.append(I)

		trans = pd.DataFrame(calc.T)
		trans = np.round(trans, 3)
		result.append(trans)

		oss = pd.DataFrame(calc.O)
		oss = np.round(oss, 3)
		result.append(oss)

	#===================================================== HIDDEN MARKOV MODEL =====================================================================



		hmm_model = Hmm(I, calc.T, calc.O)

		steps = observations.__len__()

		result.append(steps)
		hmm_model.filtering(steps, observations, observations_labels, hiddenVars_labels)
		print("\nFITERING: ")
		print(self.correspondence(hiddenVars, hmm_model.get_steps()))

		result.append(hmm_model.get_steps())
		result.append(self.correspondence(hiddenVars, hmm_model.get_steps()))
		#steps = 97
		#hmm_model.prediction(steps, observations[:90], observations_labels, hiddenVars_labels)

		print("\nVITERBI:")
		del observations[0]  # delete first element: "nullo"

		viterbi_seq = hmm_model.viterbi(observations, observations_labels, hiddenVars_labels)
		print(self.correspondence(hiddenVars, viterbi_seq))

		result.append(hmm_model.viterbi)
		result.append(self.correspondence(hiddenVars, viterbi_seq))


		return result



