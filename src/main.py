from sentiment import Sentiment
from calculator import Calculator

def main():
	sent  = Sentiment("bing", "tweets", 4)
	sent.generate_observations()

	market_transition_f = "/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/datasets/market/Market_values_ext.txt"
	market_emission_f   = "/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/datasets/market/Market_values.txt"

	calc = Calculator(market_transition_f, market_emission_f, sent.output_f)
	calc.config("variazione_5", "variazione_5", 0.001, 0.1)


if __name__ == "__main__":
	main()