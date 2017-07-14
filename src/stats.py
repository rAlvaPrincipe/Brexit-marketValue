def read(path):
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


def delta(file, tollerance):
	minore1 = 1000.0
	minore2 = 0
	values = read(file)
	deltas = []
	for count in range(0, values.__len__()):
		row = []
		row.append(values[count][0])

		if count == 0:
			row.append(0)
			row.append("nullo")
		else:
			row.append(values[count][1] - values[count - 1][1])
			if abs(row[1]) < minore1:
				minore2  = minore1
				minore1 = abs(row[1])
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

	print("MEDIA: " + str(mean))
	print ("MINORE1 "+ str(minore1))
	print ("MINORE2 "+ str(minore2))

	return deltas


def col_select(matrix, selector):
	sequence = []
	for i in range(0, matrix.__len__()):
		sequence.append(matrix[i][selector])
	return sequence


def statistics(file, tollerance):
	deltas = delta(file, tollerance)
	print "TOTAL: " + str(deltas.__len__())
	tre_mod = col_select(deltas, 2)
	sale = 0
	stabile = 0
	scende = 0
	for i in range(0, tre_mod.__len__()):
		if tre_mod[i] == "sale":
			sale += 1
		elif tre_mod[i] == "stabile":
			stabile += 1
		elif tre_mod[i] == "scende":
			scende += 1

	print 
	print "sale: " + str(sale)
	print "stabile: " + str(stabile)
	print "scende " + str(scende)

	five_mod = col_select(deltas, 5)
	saleTanto = 0
	salePoco = 0
	stabile = 0
	scendePoco = 0
	scendeTanto = 0

	for i in range(0, five_mod.__len__()):
		if five_mod[i] == "saleTanto":
			saleTanto += 1
		elif five_mod[i] == "salePoco":
			salePoco += 1
		elif five_mod[i] == "stabile":
			stabile += 1
		elif five_mod[i] == "scendePoco":
			scendePoco += 1
		elif five_mod[i] == "scendeTanto":
			scendeTanto += 1

	print 
	print "saleTanto: " + str(saleTanto)
	print "salePoco: " +  str(salePoco)
	print "stabile: " + str(stabile)
	print "scendePoco: " + str(scendePoco)
	print "scendeTanto: " + str(scendeTanto)

statistics("/home/renzo/rAlvaPrincipe/refactoring/Brexit-marketValue/data/datasets/market/Market_values_ext.txt", 0.0013)

#TODO: per capire che tolleranza usare non basta cerca di bilancia gli "stabili" con tutti gli altri... in teoria, trovato il limite (tolleranza), mi aspetto
# che o poco sopra o poco sotto non ci siano valori, nel sento se la tolleranza differenzia nettamente gli stabili dagli altri..
