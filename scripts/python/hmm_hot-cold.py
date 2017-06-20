import numpy as np

class Hmm:
    'Common base class for Hidden Markov Model'
    T=[]
    O=[]
    I=[]

    def __init__(self, T, O, I):
        self.T = T
        self.O = O
        self.I = I

    def filtering(self, steps, observations):
        out = self.I
        for i in range(0,steps):
            out = self.matrix_multiply(out, self.T) #prediction step
            out = self.matrix_multiply(out, self.diagonal(observations[i])) #update step
            out = self.normalize(out)
        return out

    def prediction(self, steps, observations):
        out = self.filtering(len(observations), observations)

        nextSteps = steps - len(observations)
        for i in range(0,nextSteps):
            out = self.matrix_multiply(out, self.T) #prediction step

        return out


    def normalize(self, list):
        sum = 0.0
        for el in list:
            sum += el

        alpha = 1.0/float(sum)

        normalized_list = []
        for el in list:
            normalized_list.append(alpha*float(el))

        return normalized_list

    def matrix_multiply(self, a, b):
        return np.dot(a,b)

    def diagonal(self, observation_index):
        transpose = np.array(self.O).transpose()
        return np.diag(transpose[observation_index])

    def stampa(self):
        print "Transition table : ", self.T,  ", Obs: ", self.O,", prob: ", self.I



transition_table = [[0.7, 0.3],
                    [0.4, 0.6,]]

observation_table = [[0.4, 0.6],
                     [0.8, 0.2]]

initial_probability = [0.5, 0.5]

hmm = Hmm(transition_table, observation_table, initial_probability)

print("Filtering:")
print(hmm.filtering(3, [0,1,1]))

print("\nPrediction:")
print(hmm.prediction(5, [0,1,1]))
