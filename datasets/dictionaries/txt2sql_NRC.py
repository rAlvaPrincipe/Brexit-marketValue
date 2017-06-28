# nrc file input
nrc_file = "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"

words = {}
sentiments = {'anger': -1, 'anticipation': 1, 'disgust': -1,
              'fear': -1, 'joy': 1, 'negative': -1,
              'positive': 1, 'sadness': -1, 'surprise': 1,
              'trust': 1}

#init the dictionary
for line in open(nrc_file):
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    line = line.split("\t")
    if len(line) > 2:
        words[line[0]] = 0

#for every line give a weight based on sentiments
for line in open(nrc_file):
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    line = line.split("\t")
    if len(line) > 2:
        #sentiments
        for i in sentiments:
            if line[1] == i and int(line[2])>0:
                words[line[0]] = int(words[line[0]]) + int(sentiments[i])
                #words[line[0]] = words[line[0]] + sentiments[i]


# add the creation table at start
f = open('NRC.sql', 'a')
table_creation = """USE experiments;
CREATE TABLE IF NOT EXISTS nrc(
    word varchar(255) NOT NULL,
    label int NOT NULL,
    PRIMARY KEY (word)
);
"""
f.write(table_creation)
f.close

#generate sql file
for word in words:
    f = open('NRC.sql', 'a')
    f.write("INSERT INTO nrc VALUES (\'"+str(word).replace("'", " \\' ")+"\', \'"+str(words[word])+"\');\n")


f.close()
