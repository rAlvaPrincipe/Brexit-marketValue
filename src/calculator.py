import sys
import copy
sys.path.append("lib/prettytable-0.7.2")
from prettytable import PrettyTable

class Calculator:
	market_transition_f = ""
	market_emission_f = ""
	sentiment_f = ""
	transition_model = []
	emission_model = []

	def __init__(self, market_transition_f, market_emission_f, sentiment_f):
		self.market_transition_f = market_transition_f
		self.market_emission_f = market_emission_f
		self.sentiment_f = sentiment_f


	# returns a nX2 matrix which associates a day with it's marke value
	# input: path = "./Brexit-marketValue/datasets/Market_values.txt""
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


    ## Returns only the column of interest of an input matrix
	## input: matrix: [["+0.34", "sale"], ["-0.002", "scende"], ...
	##		  selector = 1
	## output: ["sale", "scende, ...]
	def col_select(self, matrix, selector):
		sequence = []
		for i in range(0, matrix.__len__()):
			sequence.append(matrix[i][selector])
		return sequence


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


	## returns a nX5 matrix which associate to each day the variation and a label for the variation
	## delta(day_t) = day_t - day_t-1
	## input: values = [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
	##		  tollerance = 0.001, used to decide if a variation is to be considered "stable"
	## output: [["Dec 05, 2016", 0, "nullo", 0,00023, "pos"], ["Dec 06, 2016", -0.0139, "scende", 0,00021, "pos"]..]
	## notice that delta(day_1) is setted to the default variation and label: 0 , "nullo"
#	def delta(self, file, tollerance):
#		values = self.read(file)
#		deltas = []
#		for count in range(0, values.__len__()):
#			row = []
#			row.append(values[count][0])
#
#			if count == 0:
#				row.append(0)
#				row.append("nullo")
#			else:
#				row.append(values[count][1] - values[count - 1][1])
#				if abs(values[count][1] - values[count - 1][1]) <= tollerance:
#					row.append("stabile")
#				elif values[count][1] > values[count - 1][1]:
#					row.append("sale")
#				else:
#					row.append("scende")
#
#			row.append(values[count][1])
#			if values[count][1] >= 0:
#				row.append("pos")
#			elif values[count][1] < 0:
#				row.append("neg")
#
#			deltas.append(row)
#
#		return deltas



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


	## Returns the transition model  based on the market values and tollerance
	## input: values = [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
	##		tollerance = 0.001
	## output: [[0.25, 0.25, 0.5], [0.4, 0.2, 0.4], [0.125, 0.375, 0.5]]
	## Notice that given n days, it will not consider the head and the tail because
	## for the day_1 there is no information about the previous day, similarly for
	## the day_n there is no information about the following day
#	def build_transition_m(self, tollerance):
#		values = self.col_select(self.delta(self.market_f, tollerance), 2)
#
#		# [[saleThenSale, saleThenStabile, saleThenScende], [stabileThenSale, stabileThenStabile, stabileThenScende], ...]
#		freqs = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
#		sale = 0.0
#		scende = 0.0
#		stabile = 0.0
#
#		# Abslute frequences calculation
#		for count in range(1, values.__len__() - 1):
#			if values[count] == "sale":
#				row_index = 0
#				sale += 1
#			elif values[count] == "stabile":
#				row_index = 1
#				stabile += 1
#			elif values[count] == "scende":
#				row_index = 2
#				scende += 1
#
#			if values[count + 1] == "sale":
#				col_index = 0
#			elif values[count + 1] == "stabile":
#				col_index = 1
#			elif values[count + 1] == "scende":
#				col_index = 2
#			freqs[row_index][col_index] += 1
#
#		self.printer("FREQUENZE ASSOLUTE TRANSIZIONE", ["freqs"], ["sale", "stabile", "scende"], [sale, stabile, scende])
#		self.printer("", ["sale", "stabile", "scende"], ["sale", "stabile", "scende"], freqs)
		

		# Transition model calculation
#		transition_m = freqs
#		for i in range(0, 3):
#			if(sale > 0):
#				transition_m[0][i] = freqs[0][i] / sale
#			else:
#				transition_m[0][i] = 0.0 
#			if(stabile > 0):
#				transition_m[1][i] = freqs[1][i] / stabile
#			else:
#				transition_m[1][i] = 0.0
#			if(scende > 0):
#				transition_m[2][i] = freqs[2][i] / scende
#			else:
#				transition_m[2][i] = 0.0

#		self.printer("MODELLO DI TRANSIZIONE", ["sale", "stabile", "scende"], ["sale", "stabile", "scende"], transition_m)
#		self.transition_model = transition_m



	def build_transition_generic(self, hiddenVars, hiddenVars_labels):
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

		self.transition_model = transition_m




	## Returns the emission table. It supports any observation discretization given "observations" and "observation_labels" 
	## input: hiddenVars = [["day1", 0, "nullo"], ["day2", +0,0423, "sale"], ["day3", "-0.0001", "stabile"], ...]
	##		hiddenVars_labels = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
	##		observations =  [0, 1, 1, 0, ...]
	##		observations_labels = [["sent+", "0"], ["sent-", "1"]]
	## output: [[0.0, 1.0], [0.0, 1.0], [0.222, 0.778]]
	def build_emission_generic(self, hiddenVars, observations, hiddenVars_labels, observations_labels):
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

		self.emission_model = emission_m



	def config(self, transition_mod, emission_mod, market_tollerance, sentiment_tollerance):
		if transition_mod == "variazione":
			hiddenVars = self.col_select(self.delta(self.market_transition_f, market_tollerance), 2)
			hiddenVars_labels = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]]

		elif transition_mod == "variazione_5":
			hiddenVars = self.col_select(self.delta(self.market_transition_f, market_tollerance), 5)
			hiddenVars_labels = [["saleTanto", "saleTanto"], ["salePoco", "salePoco"], ["stabile", "stabile"], ["scendePoco", "scendePoco"], ["scedeTanto", "scendeTanto"]]

		self.build_transition_generic(hiddenVars, hiddenVars_labels)


		if emission_mod == "standard":
			observations = self.col_select( self.delta( self.sentiment_f, sentiment_tollerance), 4)
			observations_labels = [["sent+", "pos"], ["sent-", "neg"]]

		elif emission_mod == "variazione":
			observations = self.col_select( self.delta( self.sentiment_f, sentiment_tollerance), 2)
			observations_labels = [["sentSale", "sale"], ["sentStabile", "stabile"], ["sentScende", "scende"]]

		elif emission_mod == "variazione_5":
			observations = self.col_select(self.delta( self.sentiment_f, sentiment_tollerance), 5)
			observations_labels = [["sentSaleTanto", "saleTanto"], ["sentSalePoco", "salePoco"], ["sentStabile", "stabile"], ["sentScendePoco", "scendePoco"], ["sentScedeTanto", "scendeTanto"]]

		# if market dataset is different for transition and emission
		if transition_mod == "variazione":
			hiddenVars = self.col_select(self.delta(self.market_emission_f, market_tollerance), 2)
		elif transition_mod == "variazione_5":
			hiddenVars = self.col_select(self.delta(self.market_emission_f, market_tollerance), 5)

		self.build_emission_generic(hiddenVars, observations, hiddenVars_labels, observations_labels)

		

