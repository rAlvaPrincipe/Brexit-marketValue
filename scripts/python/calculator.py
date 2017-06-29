import transEmissCalc as mt
import sentiment as sm
import numpy as np

# -*- coding: utf-8 -*-
from hmm import Hmm


class Calculator():

    # builds a sequence of observation with only positive/negative sentiment
    # it uses 0 for pos and 1 for negs
    # input:
    # src_emission = "../file_path/.."
    # sentiment_discretization: 2 or 3 classes
    # sentiment_tollerance: range for sentiment neutral (only for 3 classes)
    # output 2 classes discretization: [1, 0, 0, 0, 0, 1, 0, ...]
    # output 3 classes discretization: [1, 0, 2, 0, 0, 2, 0, ...]
    def standard_sequence(self, src_emission, sentiment_discretization, sentiment_tollerance):
        sentiment = mt.extract(src_emission)
        sequence = []
        if sentiment_discretization == 2:
            for count in range(0, sentiment.__len__()):
                if sentiment[count][1] > 0:
                    sequence.extend([0])
                elif sentiment[count][1] <= 0:
                    sequence.extend([1])

        if sentiment_discretization == 3:
            for count in range(0, sentiment.__len__()):
                if sentiment[count][1] > sentiment_tollerance:
                    sequence.extend([0])
                elif sentiment[count][1] < -sentiment_tollerance:
                    sequence.extend([2])
                else:
                    sequence.extend([1])
        return sequence

    # build a sequence of observation based on sentiment variation
    # it uses 0 for sale and 1 for scende
    # input:
    # sentiment_discretization: 2 or 3 classes
    # sentiment_tollerance: range for sentiment neutral (only for 3 classes)
    # output 2 classes discretization: [1, 0, 0, 0, 0, 1, 0, ...]
    # output 3 classes discretization: [1, 0, 2, 0, 0, 2, 0, ...]
    def variation_sequence(self, src_emission, sentiment_discretization, sentiment_tollerance):
        sentiment = mt.delta_labels(src_emission, sentiment_tollerance, 1)
        sequence = []
        if sentiment_discretization == 2:
            for count in range(0, sentiment.__len__()):
                if float(sentiment[count]) > 0:
                    sequence.extend([0])
                elif float(sentiment[count]) <= 0:
                    sequence.extend([1])
        if sentiment_discretization == 3:
            for count in range(0, sentiment.__len__()):
                if float(sentiment[count]) > float(sentiment_tollerance):
                    sequence.extend([0])
                elif float(sentiment[count]) <= -float(sentiment_tollerance):
                    sequence.extend([2])
                else:
                    sequence.extend([1])
        return sequence


    # build a sequence of observation based on normalized sentiment variation
#    def boolean_normalized_sequence(self, src_emission, tollerance_norm):
#        sentiment = mt.extract(src_emission)
#        sentiment = self.normalize(sentiment)
#        sequence = []
#        for count in range(0, sentiment.__len__()):
#            if float(sentiment[count]) > float(tollerance_norm):
#                sequence.extend([0])
#            elif float(sentiment[count]) <= float(tollerance_norm):
#                sequence.extend([1])
#        return sequence
#
#    def normalize(self, list):
#        # compute alpha: the normalization variable
#        np_list=np.array(list)
#        float_list=[]
#        for count in range(0, np_list.__len__()):
#            float_list.append(float(np_list[count][1]))
#
#        max_v=max(float_list[:])
#        min_v=min(float_list[:])
#
#        normalized_list = []
#        for count in range(0, float_list.__len__()):
#            normalized_list.append((float_list[count] - min_v)/(max_v - min_v))

#        return normalized_list

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

    def compute_sentiment(self, vocabulary_request):

        ##Compute sentiment standard

        days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
                '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
                '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
                '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']
        days_sentiment = {}
        vocabulary = sm.retrieveVocabulary(vocabulary_request)

        out_file = open(vocabulary_request + "_sentiment.txt", "w")
        for i in range(0, days.__len__()):
            days_sentiment[i] = sm.day_sentiment(days[i], vocabulary)
            out_file.write(days[i] + "   " + str(days_sentiment[i]) + "\n")
            print(days_sentiment[i])
        out_file.close()

        ##Compute sentiment extended

        days_ext = [
            '2016/11/28', '2016/11/29', '2016/11/30', '2016/12/01', '2016/12/02',
            '2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
            '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
            '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
            '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30',
            '2017/01/02', '2017/01/03', '2017/01/04', '2017/01/05', '2017/01/06',]

        days_sentiment = {}
        vocabulary = sm.retrieveVocabulary(vocabulary_request)

        out_file = open(vocabulary_request + "_sentiment_ext.txt", "w")
        for i in range(0, days.__len__()):
            days_sentiment[i] = sm.day_sentiment(days_ext[i], vocabulary)
            out_file.write(days_ext[i] + "   " + str(days_sentiment[i]) + "\n")
            print(days_sentiment[i])
        out_file.close()

    def start(self, vocabulary_request, sentiment_type, market_tollerance, sentiment_tollerance, sentiment_discretization):
        days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
                '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
                '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
                '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']

        # for unix users
        #src = "../../datasets/Market_values.txt"
        #src_ext = "../../datasets/Market_values_ext.txt"

        # for valzo
        src = "D:\Dropbox\Git_Projects\Brexit-marketValue\datasets\Market_values.txt"
        src_ext = "D:\Dropbox\Git_Projects\Brexit-marketValue\datasets\Market_values_ext.txt"

        #file .._ext.txt for extended days
        #file .txt for originary days
        src_emission = vocabulary_request + "_sentiment_ext.txt"
        filtering = []
        predicted_sequence_filtering = []
        predicted_sequence_viterbi = []

        T = mt.build_transition_m(mt.extract(src_ext), market_tollerance)
        I = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]
        delta_stock = mt.delta(mt.extract(src), market_tollerance)


        if sentiment_type == "standard":

            if sentiment_discretization == 2:
                O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.standard_sequence(src_emission, 2 , sentiment_tollerance),
                                              [["sent+", "0"], ["sent-", "1"]]
                                              )
            if sentiment_discretization == 3:
                O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.standard_sequence(src_emission, 3 , sentiment_tollerance),
                                              [["sent+", "0"], ["sent=", "1"], ["sent-", "2"]]
                                              )

            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            filtering = model.filtering(19, self.standard_sequence(src_emission, sentiment_discretization, sentiment_tollerance))
            predicted_sequence_filtering = model.get_steps()
            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.standard_sequence(src_emission, sentiment_discretization, sentiment_tollerance))

        elif sentiment_type == "variation":

            if sentiment_discretization == 2:
                O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.variation_sequence(src_emission, sentiment_discretization,
                                                                      sentiment_tollerance),
                                              [["sentSale", "0"], ["sentScende", "1"]]
                                              )
            if sentiment_discretization == 3:
                O = mt.build_emission_generic(delta_stock,
                                              [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
                                              self.variation_sequence(src_emission, sentiment_discretization,
                                                                      sentiment_tollerance),
                                              [["sentSale", "0"], ["sentStabile", "1"], ["sentScende", "2"]]
                                              )
            mt.delta(mt.extract(src_emission), 0.0)
            model = Hmm(T, O, I)
            print("\n\nFiltering:")
            filtering = model.filtering(19, self.variation_sequence(src_emission, sentiment_discretization, sentiment_tollerance))
            predicted_sequence_filtering = model.get_steps()
            print("\n\nViterbi:")
            predicted_sequence_viterbi = model.viterbi(self.variation_sequence(src_emission, sentiment_discretization, sentiment_tollerance))

#        elif sentiment_type == "normalized":
#            O = mt.build_emission_m(delta_stock, self.boolean_normalized_sequence(src_emission, tollerance_norm))
#
#            model = Hmm(T, O, I)
#            print("\n\nFiltering:")
#            filtering = model.filtering(19, self.boolean_normalized_sequence(src_emission, tollerance_norm))
#            predicted_sequence_filtering = model.get_steps()
#            print("\n\nViterbi:")
#            predicted_sequence_viterbi = model.viterbi(self.boolean_normalized_sequence(src_emission, tollerance_norm))



        print("\n\nFiltering accuratezza:")
        print("L'accuratezza del filtraggio e' " +
             str(self.correspondence(delta_stock, predicted_sequence_filtering)))
        print("L'accuratezza rilassata del filtraggio e' " + str(
            self.correspondence_relaxed(delta_stock, predicted_sequence_filtering)))
        print("\n\nViterbi accuratezza:")
        print("L'accuratezza di Viterbi e' " +
              str(self.correspondence(delta_stock, predicted_sequence_viterbi)))
        print("L'accuratezza rilassata di Viterbi e' " +
              str(self.correspondence_relaxed(delta_stock, predicted_sequence_viterbi)))

        result=[]
        result.append("\nL'accuratezza del filtraggio e' " +str(self.correspondence(delta_stock, predicted_sequence_filtering)))
        result.append("\nL'accuratezza rilassata del filtraggio e' "+ str(self.correspondence_relaxed(delta_stock, predicted_sequence_filtering)))
        result.append("\nL'accuratezza di Viterbi e' " +  str(self.correspondence(delta_stock, predicted_sequence_viterbi)))
        result.append("\nL'accuratezza rilassata di Viterbi e' " + str(self.correspondence_relaxed(delta_stock, predicted_sequence_viterbi)))

        return result