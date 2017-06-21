#
# If you wanto to use on another dictionary, change AFINN-###
#

# retrive all the data
dictionary_file = "AFINN-111.txt"
afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open(dictionary_file) ]))

# add the creation table at start
f = open('AFINN-111.sql', 'a')
table_creation = """USE experiments;
CREATE TABLE IF NOT EXISTS afinn111(
    word varchar(255) NOT NULL,
    label int NOT NULL,
    PRIMARY KEY (word)
);
"""
f.write(table_creation)
f.close

# append to the file
for word in afinn:
    f = open('AFINN-111.sql', 'a')
    f.write("INSERT INTO afinn111 VALUES (\'"+str(word).replace("'", "\\'")+"\', \'"+str(afinn[word])+"\');\n")

f.close()
