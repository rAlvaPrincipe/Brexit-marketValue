from sentiment import Sentiment
from calculator import Calculator
from hmm import Hmm


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



def main():

 #========================================================== SENTIMENT =========================================================================
	
	vocabulary = "bing"
	dataset_tweets = "tweets"
	n_weeks = 4
	sent  = Sentiment(vocabulary, dataset_tweets, n_weeks)
#	sent.generate_observations()
 

 #===================================================TRANSITION AND EMISSION MODEL =============================================================

	market_transition_f = "/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/preprocessed_data/output/output_market_afinn_bing_base_afinn_market_from_ecb.europa.eu.txt"
	market_emission_f   = "/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/preprocessed_data/output_market_afinn96_market_from_investing.com.txt"
	market_emission_f = market_transition_f
	calc = Calculator(market_transition_f, market_emission_f, sent.output_f)

	transition_mod = "variazione"
	emission_mod = "variazione"
	market_tollerance = 0.0003
	sentiment_tollerance = 0.1	  ## Notice that sentiment_tollerance is irrilevant if you choouse emission_mod = standard


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

	# if market dataset is different for transition and emission
	if transition_mod == "variazione":
		hiddenVars = calc.col_select(calc.delta(calc.market_emission_f, market_tollerance), 2)
	elif transition_mod == "variazione_5":
		hiddenVars = calc.col_select(calc.delta(calc.market_emission_f, market_tollerance), 5)

	calc.build_emission_m(hiddenVars, observations, hiddenVars_labels, observations_labels)



#===================================================== HIDDEN MARKOV MODEL =====================================================================
	
	I = []
	if transition_mod == "variazione":
		I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
	elif transition_mod == "variazione_5":
		I = [0.2, 0.2, 0.2, 0.2, 0.2]

	hmm_model = Hmm(I, calc.T, calc.O)

	steps = observations.__len__()
	hmm_model.filtering(steps, observations, observations_labels, hiddenVars_labels)
	print("\nFITERING: ")
	print(correspondence(hiddenVars, hmm_model.get_steps()))

	#steps = 97
	#hmm_model.prediction(steps, observations[:90], observations_labels, hiddenVars_labels)
	
	print("\nVITERBI:")
	del observations[0]  # delete first element: "nullo"
	veterbi_seq = hmm_model.viterbi(observations, observations_labels, hiddenVars_labels)
	print(correspondence(hiddenVars, veterbi_seq))





if __name__ == "__main__":
	main()