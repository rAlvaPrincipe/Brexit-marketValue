import numpy as np
class Hmm:
	I = []
	T = []
	O = []
	steps = []

	def __init__(self, I, T, O):
		self.I = I
		self.T = T
		self.O = O



	def get_steps(self):
		labels = []
		for i in range(0, self.steps.__len__()):
			labels.append(self.steps[i][1])
		return labels

	def filtering(self, n_steps, observations, observations_labels, hiddenVars_labels):
		out = self.I

		start = 0
		if observations[0] == "nullo": # if observations are based on variazione or variazion_5 doesn't make sense to start from 0
			start = 1

		for i in range(start, n_steps):
			step =[]
			
			#prediction step
			print("\nstep: "+str(i))
			out =  np.dot(out, self.T)   
			step.append(out)
			#wich state is predicted?
			for k in range(0, out.__len__()):
				if max(out) == out[k]:
					step.append(hiddenVars_labels[k][0])
			print("_prediction: "+str(out))


			#update step
			for j in range(0, observations_labels.__len__()):
				if observations[i] == observations_labels[j][1]:
					out = np.dot(out, self.diagonal(j) )  
			step.append(out)
			print("__update: "+str(out))


			#normalization
			out = self.normalize(out) 
			step.append(out)
			for k in range(0, out.__len__()):
				if max(out) == out[k]:
					step.append(hiddenVars_labels[k][0])
			print("___normalized: "+str(out))

			self.steps.append(step)
		return out



	# normalize compute and return the normalized probability distribution
	def normalize(self, list):
		sum = 0.0
		for el in list:
			sum += el

		alpha = 1.0/float(sum)
		normalized_list = []
		for el in list:
			normalized_list.append(alpha*float(el))

		return normalized_list



	 # diagonal generate a diagonal matrix
	def diagonal(self, observation_index):
		transpose = np.array(self.O).transpose()
		return np.diag(transpose[observation_index])




	# Implements the prediction task, with filtering until observed
	def prediction(self, n_steps, observations, observations_labels, hiddenVars_labels):
		# compute the filtering until last observed
		out = self.filtering(len(observations), observations, observations_labels, hiddenVars_labels)
		# and for the other steps
		nextSteps = n_steps - len(observations)
		for i in range(0,nextSteps):
			out = np.dot(out, self.T) #prediction step
			print "step: "+str(len(observations) + i+ 1)
			print "prediction:" + str(out)
		return out