import pandas as pd
import numpy as np
import sys
import copy
sys.path.append("lib/prettytable-0.7.2")
from prettytable import PrettyTable

class Calculator:
	market_transition_f = ""
	market_emission_f = ""
	sentiment_f = ""
	T = []
	O = []


	def __init__(self, market_transition_f, market_emission_f, sentiment_f):
		self.market_transition_f = market_transition_f
		self.market_emission_f = market_emission_f
		self.sentiment_f = sentiment_f


	# returns a nX2 matrix which associates a day with it's marke value
	# input: path = file path
	# output: [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
	def read(self, path):
		data = []
		with open(path) as file:
			for line in file:
				column = []
				splitted = line.split("\t")
				date = splitted[0]
				value = float(splitted[1].strip().replace(",", "."))
				column.append(date)
				column.append(value)
				data.append(column)
		return data


    ##  Given a matrix and a column selector returns the selected column as 1D array
	def col_select(self, matrix, selector):
		sequence = []
		for i in range(0, matrix.__len__()):
			sequence.append(matrix[i][selector])
		return sequence



	## Given the labels and a matrix it prints a pretty table
	## input: header = the title of the table
	##        columns_name = the labels of the columns
	##        rows_name = the labels of the rows
	##        data = matrix with data
	def printer(self, header, columns_name, rows_name, data):
		x = PrettyTable()
		first_row = []
		row = []

		first_row.append(" ");
		for i in range(0, columns_name.__len__()):
			first_row.append(columns_name[i])
		x.field_names = first_row
	
		for i in range(0, rows_name.__len__()):
			row.append(rows_name[i])
			if isinstance(data[i], list):    #se data non e' una matrice nXm
				for j in range(0, columns_name.__len__()):
					row.append(data[i][j])
			else:                            #se data e' un array 1D
				row.append(data[i])
			x.add_row(row)
			row = []

		if header != "":
			print "\n" + header
		print x


    ## returns a nX6 matrix which associate to each day the variation and its label, the value and its label, the variation 
    ## label based on the mean of all variations
	## delta(day_t) = day_t - day_t-1
	## input: values = [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
	##		  tollerance = 0.001, used to decide if a variation is to be considered "stable"
	## output: [["Dec 05, 2016", 0, "nullo", 0,00023, "pos", "nullo"], ["Dec 06, 2016", -0.0139, "scende", 0,00021, "pos", "scendeTanto"]..]
	## notice that delta(day_1) is setted to the default variation and label: 0 , "nullo"
	def delta(self, file, tollerance):
		values = self.read(file)
		deltas = []
		for count in range(0, values.__len__()):
			row = []
			row.append(values[count][0])

			if count == 0:
				row.append(0)
				row.append("nullo")
			else:
				row.append(values[count][1] - values[count - 1][1])
				if abs(values[count][1] - values[count - 1][1]) <= tollerance:
					row.append("stabile")
				elif values[count][1] > values[count - 1][1]:
					row.append("sale")
				else:
					row.append("scende")

			row.append(values[count][1])
			if values[count][1] >= 0:
				row.append("pos")
			elif values[count][1] < 0:
				row.append("neg")
			deltas.append(row)

		sum = 0.0
		for i in range(1, deltas.__len__()):
			sum += abs(deltas[i][1])
		mean = sum/float(deltas.__len__() - 1)
		print("MEDIA: " + str(mean))

		for i in range(0, deltas.__len__()):
			temp_row = deltas[i]
			if i == 0:
				temp_row.append("nullo")
			else:
				if abs(deltas[i][1]) <= tollerance:
					temp_row.append("stabile")
				elif deltas[i][1] > 0:
					if deltas[i][1] > mean:
						temp_row.append("saleTanto")
					else:
						temp_row.append("salePoco")
				else:
					if deltas[i][1] < (0 - mean):
						temp_row.append("scendeTanto")
					else:
						temp_row.append("scendePoco")
			deltas[i] = temp_row
		return deltas



	## Generates the transition model matrix
	## input: hiddenVars = ["nullo", "sale", "scendere", "stabile", "sale", ..]
	##		  hiddenVars_labeles = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]]
	## Notice that given n days, it will not consider the head and the tail because
	## for the day_1 there is no information about the previous day, similarly for
	## the day_n there is no information about the following day
	def build_transition_m(self, hiddenVars, hiddenVars_labels):
		# inizialization
		freqs = []
		for i in range(0, hiddenVars_labels.__len__()):
			array = []
			for j in range(0, hiddenVars_labels.__len__()):
				array.append(0.0)
			freqs.append(array)

		hiddenVarsStates_freqs = []
		for i in range(0, hiddenVars_labels.__len__()):
			hiddenVarsStates_freqs.append(0.0)

		# absolute frequences calculation
		for i in range(1, hiddenVars.__len__() - 1):
			row_index = -1
			col_index = -1
			for j in range(0, hiddenVars_labels.__len__()):
				if hiddenVars[i] ==  hiddenVars_labels[j][1]:
					row_index = j
					hiddenVarsStates_freqs[j] += 1

				if hiddenVars[i + 1] == hiddenVars_labels[j][1]:
					col_index = j
			freqs[row_index][col_index] += 1			

		# transition model calculation
		transition_m = copy.deepcopy(freqs)
		for i in range(0, hiddenVars_labels.__len__()):
			for j in range(0, hiddenVars_labels.__len__()):
				if hiddenVarsStates_freqs[i] > 0:
					transition_m[i][j] = transition_m[i][j] / hiddenVarsStates_freqs[i]
				else:
					transition_m[i][j] = 0

		# print absolute frequencies
		table_labels = self.col_select(hiddenVars_labels, 0);
		self.printer("FREQUENZE ASSOLUTE TRANSIZIONE", ["freq"], table_labels, hiddenVarsStates_freqs)
		self.printer("", table_labels, table_labels, freqs)
		# print emission model
		self.printer("MODELLO DI TRANSIZIONE:", table_labels, table_labels, transition_m)

		self.T = transition_m




	## Generates the emission table. 
	## input: hiddenVars = ["nullo", "sale", "scendere", "stabile", "sale", ..]
	##		  hiddenVars_labeles = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]]
	##		  observations =  ["nullo", "scendeTanto", "stabile", "salePoco", ...]
	##		  observations_labels = [["sentSaleTanto", "saleTanto"], ["sentSalePoco", "salePoco"], ["sentStabile", "stabile"], ...]
	def build_emission_m(self, hiddenVars, observations, hiddenVars_labels, observations_labels):
		# inizialization
		freqs = []
		for i in range(0, hiddenVars_labels.__len__()):
			array = []
			for j in range(0, observations_labels.__len__()):
				array.append(0.0)
			freqs.append(array)

		hiddenVarsStates_freqs = []
		for i in range(0, hiddenVars_labels.__len__()):
			hiddenVarsStates_freqs.append(0.0)


		# absolute frequences calculation
		for i in range(0, hiddenVars.__len__()):
			for j in range(0, hiddenVars_labels.__len__()):
				if str(hiddenVars[i]) == hiddenVars_labels[j][1]:
					hiddenVarsStates_freqs[j] += 1
					for k in range(0, observations_labels.__len__()):
						if str(observations[i]) == observations_labels[k][1]:
							freqs[j][k] += 1
	
		# emission model calculation
		emission_m =  copy.deepcopy(freqs)
		for i in range(0, hiddenVars_labels.__len__()):
			for j in range(0, observations_labels.__len__()):
				if hiddenVarsStates_freqs[i] > 0:
					emission_m[i][j] = emission_m[i][j] / hiddenVarsStates_freqs[i]
				else:
					emission_m[i][j] = 0

		row_labels = self.col_select(hiddenVars_labels, 0)
		column_labels = self.col_select(observations_labels, 0)
		# print absolute frequencies
		self.printer("FREQUENZE ASSOLUTE EMISSIONE", ["freqs"], row_labels, hiddenVarsStates_freqs )
		self.printer("", column_labels, row_labels, freqs)
		# print emission model
		self.printer("MODELLO DI EMISSIONE:", column_labels, row_labels, emission_m)

		self.O = emission_m




  
		

