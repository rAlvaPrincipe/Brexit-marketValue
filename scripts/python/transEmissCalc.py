# returns a nX2 matrix which associates a day with it's marke value
# input: path = "./Brexit-marketValue/datasets/Market_values.txt""
# output: [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
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



## returns a nX3 matrix which associate to each day the variation and a label for the variation
## delta(day_t) = day_t - day_t-1
## input: values = [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
##        tollerance = 0.001, used to decide if a variation is to be considered "stable"
## output: [["Dec 05, 2016", 0, "nullo"], ["Dec 06, 2016", -0.0139, "scende"]..]
## notice that delta(day_1) is setted to the default variation and label: 0 , "nullo"
def delta(values, tollerance):
    deltas = []
    state_sequence = []
    for count in range(0, values.__len__()):
        column = []
        column.append(values[count][0])

        if count == 0:
            column.append(0)
            column.append("nullo")
            state_sequence.append("nullo")

        else:
            column.append(values[count][1] - values[count - 1][1])
            if abs(values[count][1] - values[count - 1][1]) <= tollerance:
                column.append("stabile")
                state_sequence.append("stabile")
            elif values[count][1] > values[count - 1][1]:
                column.append("sale")
                state_sequence.append("sale")
            else:
                column.append("scende")
                state_sequence.append("scende")
        deltas.append(column)
    print(state_sequence)

    return deltas


## Returns only the column of interest of the delta function output
## input: values: /...file_path/
##        tollerance = 0.001
##        selector = 1
## output: [0, +0.0045, -0.014, -0.001, ...]
def delta_labels(values, tollerance, selector):
    sequence = []
    deltas = delta(extract(values), tollerance)
    for i in range(0, deltas.__len__()):
        sequence.append(deltas[i][selector])
    return sequence


# provvisorio
def printer(array):
    for el in array:
        if isinstance(el, list):
            for el2 in el:
                print el2,
            print
        else:
            print el



## Returns the transition model  based on the market values and tollerance
## input: values = [["Dec 05, 2016", 1.1971], ["Dec 06, 2016", 1.1832], ...]
##        tollerance = 0.001
## output: [[0.25, 0.25, 0.5], [0.4, 0.2, 0.4], [0.125, 0.375, 0.5]]
## Notice that given n days, it will not consider the head and the tail because
## for the day_1 there is no information about the previous day, similarly for
## the day_n there is no information about the following day
def build_transition_m(values, tollerance):
    # [[saleThenSale, saleThenStabile, saleThenScende], [stabileThenSale, stabileThenStabile, stabileThenScende], ...]
    freqs = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    sale = 0.0
    scende = 0.0
    stabile = 0.0

    # Abslute frequences calculation
    for count in range(1, values.__len__() - 1):
        if abs(values[count][1] - values[count - 1][1]) <= tollerance:
            stabile += 1
            if abs(values[count + 1][1] - values[count][1]) <= tollerance:
                freqs[1][1] += 1
            elif values[count + 1][1] > values[count][1]:
                freqs[1][0] += 1
            else:
                freqs[1][2] += 1
        elif values[count][1] > values[count - 1][1]:
            sale += 1
            if abs(values[count + 1][1] - values[count][1]) <= tollerance:
                freqs[0][1] += 1
            elif values[count + 1][1] > values[count][1]:
                freqs[0][0] += 1
            else:
                freqs[0][2] += 1
        else:
            scende += 1
            if abs(values[count + 1][1] - values[count][1]) <= tollerance:
                freqs[2][1] += 1
            elif values[count + 1][1] > values[count][1]:
                freqs[2][0] += 1
            else:
                freqs[2][2] += 1

    # Absolute frequences print
    print("\nFREQUENZE ASSOLUTE TRANSIZIONE:")
    print "sale", sale
    print "stabile", stabile
    print "scende", scende
    print "       ", "sale", "", "stabile", "", "scende"
    print "sale   ", freqs[0][0], "   ", freqs[0][1], "   ", freqs[0][2]
    print "stabile", freqs[1][0], "   ", freqs[1][1], "   ", freqs[1][2]
    print "scende ", freqs[2][0], "   ", freqs[2][1], "   ", freqs[2][2]
    print


    # Transition model calculation
    transition_m = freqs
    for i in range(0, 3):
        if(sale > 0):
            transition_m[0][i] = freqs[0][i] / sale
        else:
            transition_m[0][i] = 0.0 
        if(stabile > 0):
            transition_m[1][i] = freqs[1][i] / stabile
        else:
            transition_m[1][i] = 0.0
        if(scende > 0):
            transition_m[2][i] = freqs[2][i] / scende
        else:
            transition_m[2][i] = 0.0

    # Transition model print
    print "MODELLO DI TRANSIZIONE:"
    print "       ", "sale", "", "Stabile", "", "scende"
    print "sale   ", transition_m[0][0], "  ", transition_m[0][1], "  ", transition_m[0][2]
    print "stabile", transition_m[1][0], "  ", transition_m[1][1], "  ", transition_m[1][2]
    print "scende ", transition_m[2][0], "  ", transition_m[2][1], "  ", transition_m[2][2]
    print

    return transition_m


## Returns the emission table. It supports any observation discretization given "observations" and "observation_labels" 
## input: hiddenVars = [["day1", 0, "nullo"], ["day2", +0,0423, "sale"], ["day3", "-0.0001", "stabile"], ...]
##        hiddenVars_labels = [["sale", "sale"], ["stabile", "stabile"], ["scende", "scende"]],
##        observations =  [0, 1, 1, 0, ...]
##        observations_labels = [["sent+", "0"], ["sent-", "1"]]
## output: [[0.0, 1.0], [0.0, 1.0], [0.222, 0.778]]
def build_emission_generic(hiddenVars, hiddenVars_labels, observations, observations_labels):
    # inizialization
    freqs = []
    for i in range(0, hiddenVars_labels.__len__()):
        array = []
        for j in range(0, observations_labels.__len__()):
            array.append(0.0)
        freqs.append(array)

    # absolute frequences calculation
    for i in range(0, hiddenVars.__len__()):
        for j in range(0, hiddenVars_labels.__len__()):
            if str(hiddenVars[i][2]) == hiddenVars_labels[j][1]:
                for k in range(0, observations_labels.__len__()):
                    if str(observations[i]) == observations_labels[k][1]:
                        freqs[j][k] += 1


    # absolute frequency calculation of hiddenVars_labels
    hiddenVarsStates_freqs = []
    for i in range(0, hiddenVars_labels.__len__()):
        freq = 0.0
        for j in range(0, observations_labels.__len__()):
            freq += freqs[i][j]
        hiddenVarsStates_freqs.append(freq)


    print("\nFREQUENZE ASSOLUTE EMISSIONE:") 
    for i in range(0, hiddenVarsStates_freqs.__len__()):
        print str(hiddenVars_labels[i][0]) + "   " + str(hiddenVarsStates_freqs[i])

    print "        ",
    for i in range(0, observations_labels.__len__()):
        print str(observations_labels[i][0]) + " ",
    print ""
    for i in range(0, hiddenVars_labels.__len__()):
        print str(hiddenVars_labels[i][0]) + "   ", 
        for j in range(0, observations_labels.__len__()):
            print str(freqs[i][j]) + "  ",
        print ""


    # emission model calculation
    emission_m = freqs
    for i in range(0, hiddenVars_labels.__len__()):
        for j in range(0, observations_labels.__len__()):
            if hiddenVarsStates_freqs[i] > 0:
                emission_m[i][j] = emission_m[i][j] / hiddenVarsStates_freqs[i]
            else:
                emission_m[i][j] = 0



    print("\nMODELLO DI EMISSIONE:")
    print "        ",
    for i in range(0, observations_labels.__len__()):
        print str(observations_labels[i][0]) + " ",
    print ""
    for i in range(0, hiddenVars_labels.__len__()):
        print str(hiddenVars_labels[i][0]) + "   ", 
        for j in range(0, observations_labels.__len__()):
            print str(emission_m[i][j]) + "  ",
        print ""

    return emission_m


# provvisorio
def build_emission_m(stock, sentiment):
    # [sale&sent+, sale&sent], [stabile&sent+, stabile&sent-] [scende&sent+, scende&sent-]
    freqs = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    sale = 0.0
    scende = 0.0
    stabile = 0.0

    for count in range(0, stock.__len__()):
        # NB: sentiment[i]=0 -> pos , sentiment[i]=1 -> neg
        if stock[count][2] == "sale":
            freqs[0][sentiment[count]] += 1
        elif stock[count][2] == "stabile":
            freqs[1][sentiment[count]] += 1
        elif stock[count][2] == "scende":
            freqs[2][sentiment[count]] += 1

    print("\nFREQUENZE ASSOLUTE EMISSIONE:")
    print "       ", "Sent+", "Sent-"
    print "sale     ", freqs[0][0], " ", freqs[0][1]
    print "stabile  ", freqs[1][0], " ", freqs[1][1]
    print "scende   ", freqs[2][0], " ", freqs[2][1]

    sale = (freqs[0][0] + freqs[0][1])
    stabile = (freqs[1][0] + freqs[1][1])
    scende = (freqs[2][0] + freqs[2][1])

    emission_m = freqs

    if(sale > 0):
        emission_m[0][0] = emission_m[0][0] / sale
        emission_m[0][1] = emission_m[0][1] / sale
    else:
        emission_m[0][0] = 0
        emission_m[0][1] = 0

    if(stabile > 0):
        emission_m[1][0] = emission_m[1][0] / stabile
        emission_m[1][1] = emission_m[1][1] / stabile
    else:
        emission_m[1][0] = 0
        emission_m[1][1] = 0
    if(scende > 0):
        emission_m[2][0] = emission_m[2][0] / scende
        emission_m[2][1] = emission_m[2][1] / scende
    else:
        emission_m[2][0] = 0
        emission_m[2][1] = 0 

    print "MODELLO DI EMISSIONE:"
    printer(emission_m)

    return emission_m
