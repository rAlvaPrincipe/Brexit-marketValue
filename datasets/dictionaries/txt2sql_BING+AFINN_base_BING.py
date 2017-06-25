

def get_afinn():
    # AFINN
    # retrive all the data
    dictionary_file = "AFINN-111.txt"
    afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open(dictionary_file) ]))

    # clear multiple words
    for word in afinn:
        afinn_word = str(word).replace("'", "\\'")
        afinn_label = str(afinn[word])

    return afinn


def get_bing():
    # BING
    # retrive all the data
    positive_file = "BING_positive_words.txt"
    negative_file = "BING_negative_words.txt"

    bing = {}
    #fill the positive words list
    for line in open(positive_file):
        if line[0] != ";" and line[0] != "\n":
            line = line.replace("\n", "")
            bing[line] = 2
    #fill the negative words list
    for line in open(negative_file):
        if line[0] != ";" and line[0] != "\n":
            line = line.replace("\n", "")
            bing[line] = -2

    return bing


## main
afinn = get_afinn()
bing = get_bing()

dictionary = {}

########da fare ciclo per 2
for i in bing:
    for j in afinn:
        if str(i) == str(j):
            dictionary[str(i)] = bing[i]
        else:
            dictionary[str(i)] = afinn[j]
            dictionary[str(j)] = bing[i]

# add the creation table at start
f = open('afinn_bing_base_bing.sql', 'a')
table_creation = """USE experiments;
CREATE TABLE IF NOT EXISTS afinn_bing_base_bing(
    word varchar(255) NOT NULL,
    label int NOT NULL,
    PRIMARY KEY (word)
);
"""
f.write(table_creation)
f.close

# and write
f = open('afinn_bing_base_bing.sql', 'a')
for word in dictionary:
    f.write("INSERT INTO afinn_bing_base_bing VALUES (\'"+str(word).replace("'", "\\'")+"\', \'"+str(dictionary[word])+"\');\n")
f.close()
