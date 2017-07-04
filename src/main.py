from sentiment import Sentiment
from calculator import Calculator

def main():
	sent  = Sentiment("bing", "tweets", 4)
	#sent.generate_observations()
	market_f  = "/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/datasets/market/Market_values.txt"
	calc = Calculator(market_f, sent.output_f)
	calc.build_transition_m(0.001)
	calc.emission_selector("standard", 0.001, 0.1)



if __name__ == "__main__":
	main()