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


	# print the label associated to prediction step o update step
	def get_steps(self):
		labels = []
		for i in range(0, self.steps.__len__()):
			labels.append(self.steps[i][1])       #1 for prediction labels, 4 for filtering labels
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



	 # diagonal generate a diagonal matrix from a emission model column
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
			print "step: "+str(len(observations) + i + 1)
			print "prediction:" + str(out)
		return out



	def viterbi(self, observations, observations_labels, hiddenVars_labels):
		matrix = []
		#first step
		step = []
		# finding the index associated to the first observations
		observation_index = -1
		for x in range(0, observations_labels.__len__()):
			if  observations[0] == observations_labels[x][1]:
				observation_index = x

		for i in range(0, self.T.__len__()):
			state_data = []
			state_data.append(-1)
			state_data.append(self.O[i][observation_index]  * self.I[i])
			step.append(state_data)
		matrix.append(step)

		#next steps
		for i in range(1, observations.__len__()):   # for each observation
			step = []
				
			# finding the index associated to the  current observation
			observation_index = -1
			for x in range(0, observations_labels.__len__()):
				if  observations[i] == observations_labels[x][1]:
					observation_index = x

			for j in range(0, self.T.__len__()):     # for each state
				state_data = []
				temp = []
				for k in range(0, self.T.__len__()): # for every possible previous state
					temp.append(matrix[i-1][k][1] * self.T[k][j] * self.O[j][observation_index])

				# keeps only the data of the max prob.
				for k in range(0, temp.__len__()):
					if temp[k] == max(temp):	
						state_data.append(k)     # keeps the index of the vertex it calculates the max prob. from
						state_data.append(temp[k])        # keeps the max possibile prob. in this state

				step.append(state_data)
			matrix.append(step)


		last_step = matrix.__len__()-1
		probs = []
		last = -1
		
		# just find the final state
		for j in range(0, matrix[last_step].__len__()):    # for each state in the i step
			probs.append(matrix[last_step][j][1]) 
		for j in range(0, probs.__len__()):
			if probs[j] == max(probs):
				last = j

		# finding indexes 
		indexes = []
		for i in reversed(range(0, matrix.__len__())):
			indexes.append(last)
			last = matrix[i][last][0]

		# replace indexes with labels
		labels = []
		for i in range(0, indexes.__len__()):
			labels.append(hiddenVars_labels[indexes[i]][0])

		# reverse order
		temp = labels
		labels = (temp[::-1])


		return labels








