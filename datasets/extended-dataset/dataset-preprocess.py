# SELECT DAYS WITH TWEETS > 1000

print("DAYS WITH TWEETS > 1000")

file = open('days_count_ordered.txt')
days_count = file.read().split("\n")
days_temp = []
for line in days_count:
    splitted_line = line.split("\t")
    if (splitted_line.__len__() == 2):  # c  qualche valore mancante quindi serve questo
        if (int(splitted_line[1]) > 1000 and splitted_line[
            0] != '2017-04-18'):  # per evitare il giorno "strano" con 220k tweet
            days_temp.append(splitted_line[0])
            print(splitted_line[0] + " " + splitted_line[1])
file.close()

# SELECT ALL MARKET DAYS

file = open('market.txt')
output = open('output_date_market.txt', "w")
market = file.read().split("\n")
market_days = []
for line in market:
    splitted_line = line.split("\t")
    market_days.append(splitted_line[0])

# SELECT DAYS WITH MARKET VALUES AND TWEETS > 1000
print("DAYS WITH MARKET VALUES")

out_days = []
for i in range(0, days_temp.__len__()):
    if (days_temp[i] in market_days):
        out_days.append(days_temp[i])
        print(days_temp[i])

# SELECT DAYS AND MARKET VALUES FOR DAYS WITH TWEETS > 1000
print("DAYS AND MARKET VALUES")
for line in market:
    splitted_line = line.split("\t")
    if (splitted_line[0] in out_days):
        output.write(splitted_line[0] + "  " + splitted_line[1] + "\n")
        print(splitted_line[0] + "  " + splitted_line[1])
file.close()
output.close()

# COMPUTE ALL VOCABULARY WITH BEST DAYS

vocabulary = ["afinn96", "afinn111", "bing", "nrc", "afinn_bing_base_bing", "afinn_bing_base_afinn"]
for i in vocabulary:
    print("vocabulary " + i + "\n")
    file = open("w999_" + i + "_tweets.txt")
    output = open("output_" + i + "_tweets.txt", "w")
    sentiment = file.read().split("\n")
    for line in sentiment:
        splitted_line = line.split("\t")
        if (splitted_line[0] in out_days):
            output.write(splitted_line[0] + "   " + splitted_line[1] + "\n")
            print(splitted_line[0] + "   " + splitted_line[1])
file.close()
output.close()
