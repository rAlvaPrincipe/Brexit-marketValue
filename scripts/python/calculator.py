import transEmissCalc as matrix
import sentiment_list_by_day as sm
import numpy as np

# -*- coding: utf-8 -*-
from hmm import Hmm


class Calculator():

    # compute the sentiment variation
    # output example: [["day1" 0], ["day2", -0.2332], ["day3", -0.003], ["day4", +1,0003]]
    def delta_emission(self, values):
        deltas = []
        for count in range(0, values.__len__()):
            column = []
            column.append(values[count][0])
            if count == 0:
                column.append("0")
            elif count > 0:
                column.append((values[count][1] - values[count - 1][1]))
            deltas.append(column)
        return deltas


    # builds a sequence of observation with only positive/negative sentiment
    # it uses 0 for pos and 1 for negs 
    # output example: [1, 0, 0, 0, 0, 1, 0, ...]
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


    # build a sequence of observation based on sentiment variation
    # output example: ["nullo", "sale", "sale", "scende", "stabile"]
    def boolean_variation_sequence2(self, source_emission, tollerance_var):
        sentiment = self.delta_emission(matrix.extract(source_emission))
        sequence = []
        for count in range(0, sentiment.__len__()):
            if count == 0:
                sequence.append("nullo")
            elif abs(sentiment[count][1]) <= float(tollerance_var):
                sequence.append("stabile")
            elif sentiment[count][1] > 0:
                sequence.append("sale")
            else:
                sequence.append("scende")

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

        # count the correspondence between the real state sequence adn the predicted sequence

    def correspondence(self, state, prediction):
        count_corr = 0.0
        for count in range(1, state.__len__()):
            if (str(state[count]) == str(prediction[count - 1])):
                count_corr += 1

        print("\n" + str(state))
        print(prediction)
        return str(count_corr / float(state.__len__() - 1))
        

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
        predicted_sequence_filtering = []
        predicted_sequence_viterbi = []

        T = matrix.build_transition_m(matrix.extract(source_ext), tollerance)
        I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
        delta_stock = matrix.delta(matrix.extract(source), tollerance)

        if sentiment_type == "standard":
            # O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance), self.boolean_standard_sequence(source_emission))
            O = matrix.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.boolean_standard_sequence(source_emission),
                                              [["sent+", "0"], ["sent-", "1"]]
                                              )
            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_standard_sequence(source_emission))
            print("L'accuratezza del filtraggio e' " + str(
                self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                    predicted_sequence_filtering)))

            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.boolean_standard_sequence(source_emission))
            print("L'accuratezza di Viterbi e' " + str(
                self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                    predicted_sequence_viterbi)))

        elif sentiment_type == "variation":
            # if you want to use sentiment variation:
            # O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance), self.boolean_variation_sequence(source_emission, tollerance_var))
            O = matrix.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.boolean_variation_sequence2(source_emission, tollerance_var),
                                              [["sentSale", "sale"], ["sentStabile", "scende"],
                                               ["sentScende", "scende"]]
                                              )
            model = Hmm(T, O, I)

            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_variation_sequence(source_emission,
                                                                                               tollerance_var))
            print("L'accuratezza del filtraggio e' " +
                  str(self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                          predicted_sequence_filtering)))

            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.boolean_variation_sequence(source_emission, tollerance_var))
            print("L'accuratezza di viterbi e' " +
                  str(self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                          predicted_sequence_viterbi)))

        elif sentiment_type == "normalized":
            # if you want to use normalized variation:
            O = matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance),
                                        self.boolean_normalized_sequence(source_emission, tollerance_norm))

            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_normalized_sequence(source_emission,
                                                                                                tollerance_norm))
            print("L'accuratezza del filtraggio e' " + str(
                self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                    predicted_sequence_filtering)))
            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(
                self.boolean_normalized_sequence(source_emission, tollerance_norm))
            print("L'accuratezza di Viterbi e' " +
                  str(self.correspondence(matrix.state_sequence(matrix.extract(source), tollerance),
                                          predicted_sequence_viterbi)))

