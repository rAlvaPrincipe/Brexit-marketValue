# retrive all the data
positive_file = "BING_positive_words.txt"
negative_file = "BING_negative_words.txt"
positive_words =  []
negative_words =  []
positive_value = 2
negative_value = -2

#fill the positive words list
for line in open(positive_file):
    if line[0] != ";" and line[0] != "\n":
        line = line.replace("\n", "")
        positive_words.append(line)
#fill the negative words list
for line in open(negative_file):
    if line[0] != ";" and line[0] != "\n":
        line = line.replace("\n", "")
        negative_words.append(line)

#WARNING! Three words (envious,enviously,enviousness ) are positive AND negative.
#we remove these words from positive_words list
for i in positive_words:
        if str(i) in negative_words:
            positive_words.remove(str(i))

# add the creation table at start
f = open('BING.sql', 'a')
table_creation = """USE experiments;
CREATE TABLE IF NOT EXISTS bing(
    word varchar(255) NOT NULL,
    label int NOT NULL,
    PRIMARY KEY (word)
);
"""
f.write(table_creation)
f.close

# append positive words
for word in positive_words:
    f = open('BING.sql', 'a')
    f.write("INSERT INTO bing VALUES (\'"+str(word).replace("'", "\\'")+"\', \'"+str(positive_value)+"\');\n")

# append negative words
for word in negative_words:
    f = open('BING.sql', 'a')
    f.write("INSERT INTO bing VALUES (\'"+str(word).replace("'", "\\'")+"\', \'"+str(negative_value)+"\');\n")


f.close()
