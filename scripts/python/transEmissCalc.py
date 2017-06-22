
# prende in input il dataset, legge riga per riga e restituisce una matrice nx2
#  ove alla prima riga ci sono i giorni e alla seconda i valori corripondenti
def extract(path):
    data = []
    with open(path) as file:
        for line in file:
            column = []
            splitted = line.split("  ")
            date = splitted[0]
            value = float(splitted[1].strip().replace(",", "."))
            column.append(date)
            column.append(value)
            data.append(column)
    return data

### TRANSITION

# prende in input l'output di extract e ritorna una matrice (n-1)x2 dove alla
# prima riga ci sono i  giorni e alla seconda i delta
# delta(day_t) = day_t - day_t-1
def delta(values, tollerance):
    deltas = []
    for count in range(1, values.__len__()):
        column = []
        column.append(values[count][0])
        column.append(values[count][1] - values[count - 1][1])
        if abs(values[count][1] - values[count - 1][1]) <= tollerance:
            column.append("stabile")
        elif values[count][1] > values[count - 1][1]:
            column.append("sale")
        else:
            column.append("scende")
        deltas.append(column)

    return deltas


def printer(array):
    for el in array:
        if isinstance(el, list):
            for el2 in el:
                print el2,
            print
        else:
            print el


# prende in input l'output di extract e ritorna una matrice mx2 che associa ad
# ogni possibile transizione la sua probabilita. Inoltre stampa le frequenze
# assolute di tali transizioni nel dataset
def build_transition_m(data, tollerance):
    # [saleThenSale, saleThenStabile, saleThenScende], [stabileThenSale, stabileThenStabile, stabileThenScende], ..
    freqs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  
    sale = 0
    scende = 0
    stabile = 0


    for count in range(1, data.__len__() - 1):
        if abs(data[count][1] - data[count - 1][1]) <= tollerance:
            stabile += 1
            if abs(data[count + 1][1] - data[count][1]) <= tollerance:
                freqs[1][1] += 1
            elif data[count + 1][1] > data[count][1]:
                freqs[1][0] += 1
            else:
                freqs[1][2] += 1
        elif data[count][1] > data[count - 1][1]:
            sale += 1
            if abs(data[count + 1][1] - data[count][1]) <= tollerance:
                freqs[0][1] += 1
            elif data[count + 1][1] > data[count][1]:
                freqs[0][0] += 1
            else:
                freqs[0][2] += 1
        else:
            scende += 1
            if abs(data[count + 1][1] - data[count][1]) <= tollerance:
                freqs[2][1] += 1
            elif data[count + 1][1] > data[count][1]:
                freqs[2][0] += 1
            else:
                freqs[2][2] += 1

    print("\nFREQUENZE ASSOLLUTE:")
    print "stabile", stabile
    print "sale", sale
    print "scende", scende
    printer(freqs)
    print

    transition_m = freqs

    for i in range(0, 3):
        transition_m[0][i] = (float(freqs[0][i]) / float(sale))
        transition_m[1][i] = (float(freqs[1][i]) / float(stabile))
        transition_m[2][i] = (float(freqs[2][i]) / float(scende))

    print "MODELLO DI TRANSIZIONE:"
    print "       ", "sale" ,"  " , "Stabile" ,"  " , "scende"
    print "sale   ", transition_m[0][0]," ", transition_m[0][1], transition_m[0][2]
    print "stabile", transition_m[1][0]," ", transition_m[1][1], transition_m[1][2]
    print "scende ", transition_m[2][0]," ", transition_m[2][1], transition_m[2][2]

    return transition_m

### EMISSION

def delta_emission(values):
    deltas = []
    for count in range(0, values.__len__()):
        column = []
        column.append(values[count][0])
        if count == 0:
            column.append("0")
        if count != 0:
            column.append((values[count - 1][1] - values[count][1])/(values[count - 1][1]))
        deltas.append(column)
    return deltas

def build_emission_m(stock , sentiment):
    # [saleThenSale, saleThenStabile, saleThenScende], [stabileThenSale, stabileThenStabile, stabileThenScende], ..
    freqs = [[0, 0], [0, 0], [0, 0]]  
    sale = 0
    scende = 0
    stabile = 0
    count = 0

    for count in range(0, stock.__len__()):
        # NB: sentiment[i]=0 -> pos , sentiment[i]=1 -> neg
        if stock[count][2] == "sale":
            freqs[0][sentiment[count]] += 1
        elif stock[count][2] == "stabile":
            freqs[1][sentiment[count]] += 1
        elif stock[count][2] == "scende":
            freqs[2][sentiment[count]] += 1


    print("\nFREQUENZE ASSOLUTE:")
    print "       ", "Sent+" , "Sent-"
    print "sale", freqs[0][0]," ", freqs[0][1]
    print "stabile   ", freqs[1][0]," ", freqs[1][1]
    print "scende ", freqs[2][0]," ", freqs[2][1]


    n = stock.__len__() - 1
    n = float(n)

    sale = freqs[0][0] + freqs[0][1]
    stabile = (freqs[1][0] + freqs[1][1])
    scende = (freqs[2][0] + freqs[2][1])
    for i in range(0, 3):
        for j in range(0, 2):
            freqs[i][j] = float(freqs[i][j])

    emission_m = freqs

    emission_m[0][0] = emission_m[0][0] / sale
    emission_m[0][1] = emission_m[0][1] / sale
    emission_m[1][0] = emission_m[1][0] / stabile
    emission_m[1][1] = emission_m[1][1] / stabile
    emission_m[2][0] = emission_m[2][0] / scende
    emission_m[2][1] = emission_m[2][1] / scende



    print "MODELLO DI EMISSIONE:"
    printer(emission_m)

    return emission_m
