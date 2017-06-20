import numpy as np

# Hmm class describe a Hidden Markov Model
class Hmm:
    'Common base class for Hidden Markov Model'
    T=[] # Transition table
    O=[] # Observation table
    I=[] # Initial probability

    # __init__ constructor
    def __init__(self, T, O, I):
        self.T = T
        self.O = O
        self.I = I

    # filtering describe the filtering task, return the probability distribution
    def filtering(self, steps, observations):
        out = self.I

        for i in range(0,steps):
            print("\nstep: "+str(i))
            out = self.matrix_multiply(out, self.T) #prediction step
            print("_prediction: "+str(out))
            out = self.matrix_multiply(out, self.diagonal(observations[i])) #update step
            print("__update: "+str(out))
            out = self.normalize(out) #normalization
            print("___normalized: "+str(out))
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



transition_table = [[0.25, 0.25, 0.50],
                    [0.40, 0.20, 0.40],
                    [0.11, 0.33, 0.56]]

observation_table = [[0.00, 1.00],
                     [0.40, 0.60],
                     [0.56, 0.44]]

initial_probability = [0.33, 0.33, 0.33]

hmm = Hmm(transition_table, observation_table, initial_probability)

print("Filtering:")
print(hmm.filtering(15, [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1]))

print("\nPrediction:")
print(hmm.prediction(5, [0,1,1]))
