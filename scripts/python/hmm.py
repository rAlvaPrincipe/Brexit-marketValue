import numpy as np
# -*- coding: utf-8 -*-

# Hmm class describe a Hidden Markov Model
class Hmm:
    'Common base class for Hidden Markov Model'
    T=[] # Transition table
    O=[] # Observation table
    I=[] # Initial probability
    Steps=[] #labelled steps [ #step1 [ #previsione[p1,p2,p3, sale], #aggiornamento[p1,p2,p3], #normalizzazione [p1,p2,p3]], #step2...]
    Steps_complete = [] #labelled steps [#sale[best_precedent, p], #stabilee[best_precedent, p],.....]
    Viterbi_Steps=[] #labelled steps [#sale[best_precedent, p], #stabilee[best_precedent, p],.....]
    # __init__ constructor
    def __init__(self, T, O, I):
        self.T = T
        self.O = O
        self.I = I

    # filtering describe the filtering task, return the probability distribution
    def filtering(self, steps, observations):
        result=[]
        out = self.I
        for i in range(0,steps):
            print("\nstep: "+str(i))
            out = self.matrix_multiply(out, self.T) #prediction step
            #wich state is predicted?
            step = []
            step_complete =[]
            if(max(out) == out[0]):
                step.append(out)
                step.append("sale")
                step_complete.append(out)
                step_complete.append("sale")
            elif (max(out) == out[1]):
                step.append(out)
                step.append("stabile")
                step_complete.append(out)
                step_complete.append("stabile")
            elif (max(out) == out[2]):
                step.append(out)
                step.append("scende")
                step_complete.append(out)
                step_complete.append("scende")

            print("_prediction: "+str(out))

            out = self.matrix_multiply(out, self.diagonal(observations[i])) #update step
            step_complete.append(out)
            print("__update: "+str(out))

            out = self.normalize(out) #normalization
            step_complete.append(out)
            print("___normalized: "+str(out))

            self.Steps.append(step)
            self.Steps_complete.append(step_complete)
        return out

    # prediction describe the prediction task, with filtering until observed
    def prediction(self, steps, observations):
        # compute the filtering until last observed
        out = self.filtering(len(observations), observations)
        # and for the other steps
        nextSteps = steps - len(observations)
        for i in range(0,nextSteps):
            out = self.matrix_multiply(out, self.T) #prediction step

        return out

    # normalize compute and return the normalized probability distribution
    def normalize(self, list):
        sum = 0.0
        for el in list:
            sum += el

        # compute alpha: the normalization variable
        alpha = 1.0/float(sum)

        normalized_list = []
        for el in list:
            normalized_list.append(alpha*float(el))

        return normalized_list

    # matrix_multiply wrap the numpy dot(a,b) matrix multiplication
    def matrix_multiply(self, a, b):
        return np.dot(a,b)

    # diagonal generate a diagonal matrix
    def diagonal(self, observation_index):
        transpose = np.array(self.O).transpose()
        return np.diag(transpose[observation_index])

    # describe print the internal variables of the Hidden Markov Model
    def describe(self):
        print "Transition table : ", self.T,  ", Obs: ", self.O,", prob: ", self.I

    # get_steps return the steps of filtering
    def get_steps(self):
        steps_list = []
        for step in self.Steps:
            steps_list.append(step[1])

        return steps_list

    def get_steps_complete(self):
        steps_list = []
        for step in self.Steps_complete:
            steps_list.append(step)

        return steps_list
    ####VITERBI


    def viterbi(self, observations_seq):

        # il modello e' costituito da 3 vettori che rappresentano le probabilita per ogni stato
        p_sale = []
        p_stabile = []
        p_scende = []

        # inizializzo i vettori moltiplicando I per la prima osservazione
        # ogni stato viene inserito come coppia [stato precedente, probabilita]
        # il primo stato precedente viene assegnato a 0
        p_sale.append([0, float(self.O[0][observations_seq[0]]) * float(self.I[0])])
        p_stabile.append([0, float(self.O[1][observations_seq[0]] * float(self.I[1]))])
        p_scende.append([0, float(self.O[2][observations_seq[0]] * float(self.I[2]))])

        # calcolo in avanti le probabilita
        for i in range(1, observations_seq.__len__()):

            # calculate for state "sale" (sale = 0) stato_prec*T*O
            p_sale_temp = float(p_sale[i - 1][1]) * self.T[0][0] * self.O[0][observations_seq[i]]
            p_stabile_temp = float(p_stabile[i - 1][1]) * self.T[0][1] * self.O[1][observations_seq[i]]
            p_scende_temp = float(p_scende[i - 1][1]) * self.T[0][2] * self.O[2][observations_seq[i]]

            # seleziono il massimo e lo inserisco nel vettore
            val_max = max(p_sale_temp, p_stabile_temp, p_scende_temp)

            if (val_max == p_sale_temp):
                p_sale.append([0, p_sale_temp])
            elif (val_max == p_stabile_temp):
                p_sale.append([1, p_stabile_temp])
            elif (val_max == p_scende_temp):
                p_sale.append([2, p_scende_temp])

            # calculate for state stabile (stabile = 1)
            p_sale_temp = float(p_sale[i - 1][1]) * self.T[1][0] * self.O[0][observations_seq[i]]
            p_stabile_temp = float(p_stabile[i - 1][1]) * self.T[1][1] * self.O[1][observations_seq[i]]
            p_scende_temp = float(p_scende[i - 1][1]) * self.T[1][2] * self.O[2][observations_seq[i]]

            val_max = max(p_sale_temp, p_stabile_temp, p_scende_temp)

            if (val_max == p_sale_temp):
                p_stabile.append([0, p_sale_temp])
            elif (val_max == p_stabile_temp):
                p_stabile.append([1, p_stabile_temp])
            elif (val_max == p_scende_temp):
                p_stabile.append([2, p_scende_temp])

            # calculate for state scende (stabile = 2)
            p_sale_temp = float(p_sale[i - 1][1]) * self.T[2][0] * self.O[0][observations_seq[i]]
            p_stabile_temp = float(p_stabile[i - 1][1]) * self.T[2][1] * self.O[1][observations_seq[i]]
            p_scende_temp = float(p_scende[i - 1][1]) * self.T[2][2] * self.O[2][observations_seq[i]]

            val_max = max(p_sale_temp, p_stabile_temp, p_scende_temp)

            if (val_max == p_sale_temp):
                p_scende.append([0, p_sale_temp])
            elif (val_max == p_stabile_temp):
                p_scende.append([1, p_stabile_temp])
            elif (val_max == p_scende_temp):
                p_scende.append([2, p_scende_temp])

        print("\nsale :" + str(p_sale) +
              "\nstabile :" + str(p_stabile) +
              "\nscende :" + str(p_scende))
        viterbi_step=[]
        viterbi_step.append(p_sale)
        viterbi_step.append(p_stabile)
        viterbi_step.append(p_scende)
        self.Viterbi_Steps.append(viterbi_step)

        best_sequence = []
        j = 0
        state = 0

        # scelgo lo stato da cui partire per il backward
        val_max = max(p_sale[j][1], p_stabile[j][1], p_scende[j][1])

        # inserisco lo stato di partenza
        if (val_max == p_sale[observations_seq.__len__() - 1][1]):
            best_sequence.append("sale")
            state = p_sale[observations_seq.__len__() - 1][0]
        elif (val_max == p_stabile[observations_seq.__len__() - 1][1]):
            best_sequence.append("stabile")
            state = p_stabile[observations_seq.__len__() - 1][0]
        elif (val_max == p_scende[observations_seq.__len__() - 1][1]):
            best_sequence.append("scende")
            state = p_scende[observations_seq.__len__() - 1][0]

        # percorro all'indietro i 3 vettori per seguire il percorso migliore
        for count in range(1, observations_seq.__len__()):
            j = observations_seq.__len__() - count
            next_state = 0
            if (state == 0):
                best_sequence.append("sale")
                next_state = p_sale[j][0]
            elif (state == 1):
                best_sequence.append("stabile")
                next_state = p_stabile[j][0]
            elif (state == 2):
                best_sequence.append("scende")
                next_state = p_scende[j][0]

            state = next_state

        # ritorno la sequenza invertita
        return (best_sequence[::-1])

    def get_viterbi_steps(self):

        return self.Viterbi_Steps
## how to use: example code

# transition_table = [[0.25, 0.25, 0.50],
#                    [0.40, 0.20, 0.40],
#                    [0.11, 0.33, 0.56]]
#
# observation_table = [[0.00, 1.00],
#                      [0.40, 0.60],
#                      [0.56, 0.44]]
#
# initial_probability = [0.33, 0.33, 0.33]
#
# hmm = Hmm(transition_table, observation_table, initial_probability)
#
#print("Filtering:")
#print(hmm.filtering(15, [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1]))

#print(hmm.get_steps())

#print("\nPrediction:")
#print(hmm.prediction(5, [0,1,1]))
