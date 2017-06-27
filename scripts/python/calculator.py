import transEmissCalc as mt
import sentiment as sm
import numpy as np

# -*- coding: utf-8 -*-
from hmm import Hmm


class Calculator():

    # builds a sequence of observation with only positive/negative sentiment
    # it uses 0 for pos and 1 for negs 
    # input: source_emission = "../file_path/.."
    # output: [1, 0, 0, 0, 0, 1, 0, ...]
    def boolean_standard_sequence(self, source_emission):
        sentiment = mt.extract(source_emission)
        sequence = []
        for count in range(0, sentiment.__len__()):
            if sentiment[count][1] > 0:
                sequence.extend([0])
            elif sentiment[count][1] <= 0:
                sequence.extend([1]) 

        return sequence

    # build a sequence of observation based on sentiment variation
    # it uses 0 for sale and 1 for scende
    def boolean_variation_sequence(self, source_emission, tollerance_var):
        sentiment = mt.delta_labels(source_emission, tollerance_var, 1) 
        sequence = []
        for count in range(0, sentiment.__len__()):
            if float(sentiment[count]) > float(tollerance_var):
                sequence.extend([0])
            elif float(sentiment[count]) <= float(tollerance_var):
                sequence.extend([1])
        return sequence


    # build a sequence of observation based on normalized sentiment variation
    def boolean_normalized_sequence(self, source_emission, tollerance_norm):
        sentiment = mt.extract(source_emission)
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
            if (str(state[count][2]) == str(prediction[count - 1])):
                count_corr += 1

        print "[",
        for i in range(0, state.__len__()):
            print( str(state[i][2]) +" "),
        print  "]"

        print(prediction)
        return str(count_corr / float(state.__len__() - 1))

    def correspondence_relaxed(self, state, prediction):
        count_corr = 0.0
        for count in range(1, state.__len__()):
            if (str(state[count][2]) == "sale" and (
                    str(prediction[count - 1]) == "sale" or str(prediction[count - 1]) == "stabile")):
                count_corr += 1
            elif (str(state[count][2]) == "scende" and (
                    str(prediction[count - 1]) == "scende" or str(prediction[count - 1]) == "stabile")):
                count_corr += 1
            elif (str(state[count][2]) == "stabile" and (
                        str(prediction[count - 1]) == "stabile" or str(prediction[count - 1]) == "sale" or str(
                    prediction[count - 1]) == "scende")):
                count_corr += 1
        
        print "[",
        for i in range(0, state.__len__()):
            print( str(state[i][2]) +" "),
        print  "]"

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

        T = mt.build_transition_m(mt.extract(source_ext), tollerance)
        I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
        delta_stock = mt.delta(mt.extract(source), tollerance)

        if sentiment_type == "standard":
            O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.boolean_standard_sequence(source_emission),
                                              [["sent+", "0"], ["sent-", "1"]]
                                              )
            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_standard_sequence(source_emission))
            print("L'accuratezza del filtraggio e' " + str(
                self.correspondence(mt.delta(mt.extract(source), tollerance), predicted_sequence_filtering)))
            
            print("L'accuratezza rilassata del filtraggio e' " + str(
                self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                            predicted_sequence_filtering)))

            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.boolean_standard_sequence(source_emission))
            print("L'accuratezza di Viterbi e' " + str(
                self.correspondence(mt.delta(mt.extract(source), tollerance),
                                    predicted_sequence_viterbi)))
            print("L'accuratezza rilassata di Viterbi e' " + str(
                self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                            predicted_sequence_viterbi)))
        elif sentiment_type == "variation":
            O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              mt.delta_labels(source_emission, tollerance_var, 2),
                                              [["sentSale", "sale"], ["sentStabile", "scende"],
                                               ["sentScende", "scende"]]
                                              )
            mt.delta(mt.extract(source_emission), 0.0)
            model = Hmm(T, O, I)

            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_variation_sequence(source_emission,
                                                                                               tollerance_var))
            print("L'accuratezza del filtraggio e' " +
                  str(self.correspondence(mt.delta(mt.extract(source), tollerance),
                                          predicted_sequence_filtering)))
            print("L'accuratezza rilassata del filtraggio e' " +
                  str(self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                                  predicted_sequence_filtering)))

            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.boolean_variation_sequence(source_emission, tollerance_var))
            print("L'accuratezza di viterbi e' " +
                  str(self.correspondence(mt.delta(mt.extract(source), tollerance),
                                          predicted_sequence_viterbi)))
            print("L'accuratezza rilassata di viterbi e' " +
                  str(self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                                  predicted_sequence_viterbi)))

        elif sentiment_type == "normalized":
            O = mt.build_emission_m(mt.delta(mt.extract(source), tollerance),
                                        self.boolean_normalized_sequence(source_emission, tollerance_norm))

            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            predicted_sequence_filtering = model.filtering(19, self.boolean_normalized_sequence(source_emission,
                                                                                                tollerance_norm))
            print("L'accuratezza del filtraggio e' " + str(
                self.correspondence(mt.delta(mt.extract(source), tollerance),
                                    predicted_sequence_filtering)))
            print("L'accuratezza rilassata del filtraggio e' " + str(
                self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                            predicted_sequence_filtering)))
            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(
                self.boolean_normalized_sequence(source_emission, tollerance_norm))
            print("L'accuratezza di Viterbi e' " +
                  str(self.correspondence(mt.delta(mt.extract(source), tollerance),
                                          predicted_sequence_viterbi)))
            print("L'accuratezza rilassata di Viterbi e' " +
                  str(self.correspondence_relaxed(mt.delta(mt.extract(source), tollerance),
                                                  predicted_sequence_viterbi)))


