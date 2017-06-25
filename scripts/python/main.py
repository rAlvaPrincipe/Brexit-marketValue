import transEmissCalc as matrix
import sentiment_list_by_day as sm
import pygtk
import numpy as np

pygtk.require('2.0')
import gtk
from hmm import Hmm


class Interface:
    vocabulary = []
    vocabulary_request = ""

    def calcola(self, widget, data=None):
        calculator = Calculator()
        # use default sentiment_type = variation
        calculator.start(self.vocabulary_request, "variation", 0.001, 0, 0.6)

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

        # Another callback

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def callback(self, widget, data=None):
        if (widget.get_active() == True):
            self.vocabulary_request = data
        if (widget.get_active() == False):
            self.vocabulary_rdequest = ""

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        vbox = gtk.VBox(True, 2)
        self.window.add(vbox)

        button = gtk.CheckButton("afinn96")
        button.connect("toggled", self.callback, "afinn96")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("afinn111")
        button.connect("toggled", self.callback, "afinn111")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("bing")
        button.connect("toggled", self.callback, "bing")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("nrc")
        button.connect("toggled", self.callback, "nrc")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.Button("Calcola")
        button.connect("clicked", self.calcola, None)
        button.connect_object("clicked", gtk.Widget.destroy, self.window)
        vbox.pack_start(button, True, True, 2)
        button.show()

        vbox.show()
        self.window.show()

    # All PyGTK applications must have a gtk.main(). Control ends here
    # and waits for an event to occur (like a key press or mouse event).
    # If the program is run directly or passed as an argument to the python
    # interpreter then create a HelloWorld instance and show it
    def main(self):
        gtk.main()


class Calculator:
    # compute the sentiment variation
    def delta_emission(self, values):
        deltas = []
        for count in range(0, values.__len__()):
            column = []
            column.append(values[count][0])
            if count == 0:
                column.append("0")
            if count != 0:
                column.append((values[count][1] - values[count - 1][1]))
            deltas.append(column)
        return deltas

    # builds a sequence of observation with only positive/negative sentiment
    # it uses 0 for pos and 1 for negs 
    def boolean_standard_sequence(self, source_emission):
        sentiment = matrix.extract(source_emission)
        sequence = []
        for count in range(0, sentiment.__len__()):
            if float(sentiment[count][1]) > 0:
                sequence.extend([0])
            elif float(sentiment[count][1]) <= 0:
                sequence.extend([1])

        
        return sequence

    # build a sequence of observation based on sentiment variation
    # it uses 0 for sale and 1 for scende
    def boolean_variation_sequence(self, source_emission, tollerance_var):
        sentiment = self.delta_emission(matrix.extract(source_emission))
        sequence = []
        for count in range(0, sentiment.__len__()):
            if float(sentiment[count][1]) > float(tollerance_var):
                sequence.extend([0])
            elif float(sentiment[count][1]) <= float(tollerance_var):
                sequence.extend([1])
        return sequence

    # build a sequence of observation based on normalized sentiment variation
    def boolean_normalized_sequence(self, source_emission, tollerance_norm):

        sentiment = matrix.extract(source_emission)
        sentiment = self.normalize(sentiment)
        sequence = []
        for count in range(0, sentiment.__len__()):
            if float(sentiment[count]) > float(tollerance_norm):
                sequence.extend([0])
            elif float(sentiment[count]) <= float(tollerance_norm):
                sequence.extend([1])
        return sequence

    def normalize(self, list):
        # compute alpha: the normalization variable
        np_list=np.array(list)
        float_list=[]
        for count in range(0, np_list.__len__()):
            float_list.append(float(np_list[count][1]))

        max_v=max(float_list[:])
        min_v=min(float_list[:])

        normalized_list = []
        for count in range(0, float_list.__len__()):
            normalized_list.append((float_list[count] - min_v)/(max_v - min_v))

        return normalized_list

    #count the correspondence between the real state sequence adn the predicted sequence
    def correspondence(self, state, prediction):
        count_corr = 0.0
        for count in range(1, state.__len__()):
            if(str(state[count])==str(prediction[count-1])):
                count_corr += 1

        print("\nThe correspondence obteined is "+str(count_corr/ float(state.__len__() - 1)))
        print(state)
        print(prediction)


    def start(self, vocabulary_request, sentiment_type, tollerance, tollerance_var, tollerance_norm):
        days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
                '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
                '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
                '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']
        days_sentiment = {}

        vocabulary = sm.retrieveVocabulary(vocabulary_request)

        out_file = open("Sentiment.txt", "w")
        for i in range(0, days.__len__()):
            days_sentiment[i] = sm.day_sentiment(days[i], vocabulary)
            out_file.write(days[i] + "   " + str(days_sentiment[i]) + "\n")
            print(days_sentiment[i])
        out_file.close()

        source = "../../datasets/Market_values.txt"
        source_ext = "../../datasets/Market_values_ext.txt"

        # for valzo
        #source = "D:\Dropbox\Git_Projects\Brexit-marketValue\datasets\Market_values.txt"
        #source_ext = "D:\Dropbox\Git_Projects\Brexit-marketValue\datasets\Market_values_ext.txt"

        source_emission = "Sentiment.txt"

        predicted_sequence=[]
        if sentiment_type == "standard":
            T = matrix.build_transition_m(matrix.extract(source_ext), tollerance)
            O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance), self.boolean_standard_sequence(source_emission))
            I = [1.0/3.0, 1.0/3.0, 1.0/3.0]
            model = Hmm(T, O, I)
            print("Filtering:")
            predicted_sequence = model.filtering(19, self.boolean_standard_sequence(source_emission))
            self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance), predicted_sequence)

        elif sentiment_type == "variation":
            # if you want to use sentiment variation:
            T = matrix.build_transition_m(matrix.extract(source_ext), tollerance)
            O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance), self.boolean_variation_sequence(source_emission, tollerance_var))
            I = [1.0/3.0, 1.0/3.0, 1.0/3.0]
            model = Hmm(T, O, I)
            print("Filtering:")
            predicted_sequence = model.filtering(19, self.boolean_variation_sequence(source_emission, tollerance_var))
            self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance), predicted_sequence)

        elif sentiment_type == "normalized":
            # if you want to use normalized variation:
            T = matrix.build_transition_m(matrix.extract(source_ext), tollerance)
            O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance), self.boolean_normalized_sequence(source_emission, tollerance_norm))
            I = [1.0/3.0, 1.0/3.0, 1.0/3.0]
            model = Hmm(T, O, I)
            print("\nFiltering:")
            predicted_sequence= model.filtering(19, self.boolean_normalized_sequence(source_emission, tollerance_norm))
            self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance), predicted_sequence)


if __name__ == "__main__":
    # USE THIS IF YOU WANT GUI

    # interface = Interface()
    # interface.main()

    # USE THIS IF YOU DON'T WANT GUI

    calculator = Calculator()
    # vocabulary = afinn96, afinn111, bing, nrc, afinn_bing_base_bing, afinn_bing_base_afinn
    # sentiment_type = standard, variation, normalized
    # tollerance for 3 type of discretization
    calculator.start("bing", "standard", 0.001, 0, 0.7)