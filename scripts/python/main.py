from gui import Interface
from calculator import Calculator

if __name__ == "__main__":
        # USE THIS IF YOU WANT GUI

       #  interface = Interface()
       #  interface.main()

        # USE THIS IF YOU DON'T WANT GUI

        calculator = Calculator()
        # vocabulary = afinn96, afinn111, bing, nrc, afinn_bing_base_bing, afinn_bing_base_afinn
        # sentiment_type = standard, variation, normalized
        # tollerance for 3 type of discretization
        vocabular="afinn_bing_base_bing"
        calculator.compute_sentiment(vocabular)
        #calculator.start(vocabular, "variation",0.001, 0.2, 3)
