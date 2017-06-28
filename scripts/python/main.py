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
        calculator.start("bing", "variation",0.001, 0.2, 3)
