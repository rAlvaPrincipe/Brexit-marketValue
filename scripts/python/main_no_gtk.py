import sys
import MySQLdb
import math
import transEmissCalc as matrix

######
# This version of main is for r3vit that use macOS without pygtk
# <3
######

#retrieve_dictionary return a dictionary of words with weighted values of sentiment
#e.g.: {'hate': -5, 'love': +5, 'abacus': 0}
def retrieve_dictionary(name):
        dictionary={}
        # Connect
        db = MySQLdb.connect(host="127.0.0.1",
                             user="root",
                             passwd="root",
                             db="experiments")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        query=""

        #check what dictionary is requested
        if name == "nrc":
            query = "SELECT word, label FROM nrc"
        elif name == "bing":
            query = "SELECT word, label FROM bing"
        elif name == "afinn96":
            query = "SELECT word, label FROM afinn96"
        elif name == "afinn111":
            query = "SELECT word, label FROM afinn111"

        #exec the query and populate the dictionary
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            #populate the dictionary
            for row in results:
               w = row[0]
               l = int(row[1])
               dictionary[w] = l

        except:
           print("Error: dictionary - unable to fetch data.")

        # Close the connection
        db.close()

        return dictionary

# sentiment(tweet, dictionary) return an integer value for the the sentiment of the tweet
# calculated as sum of all the values of labelled words in the tweet
def sentiment(tweet, dictionary):
    #sentiment value
    value = 0

    #split tweet in words using ' '(space) character
    words = tweet.split(' ')
    #remove non alpha characters from every word
    for i in range (0, words.__len__()):
        words[i] = filter(str.isalpha, words[i])
        if (dictionary.get(words[i]) != None):
            value += int(dictionary.get(words[i]))

    return value


# day_sentiment(day, dictionary) return a float as total sentiment of the day
# calculated as log((sum(positive_tweets))/(sum(negative_tweets)))
def day_sentiment(day,dictionary):
    #set pos and neg = 0 for formula log((sum(positive_tweets))/(sum(negative_tweets)))
    pos = 0
    neg = 0

    # Connect
    db = MySQLdb.connect(host="127.0.0.1",
                        user="root",
                        passwd="root",
                        db="experiments")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL SELECT statement where tweet_date is "day" (e.g. 2016-12-28)
    try:
        cursor.execute("SELECT tweet FROM tweets WHERE tweet_date = \'"+day+"\';")
        tweets = cursor.fetchall()
        for tweet in tweets:
            # calculate the sentiment of the single tweet
            score = sentiment(tweet[0],dictionary)

            # score of single tweet will be counted as boolean (< or > 0)
            if score > 0:
                pos += 1
            if score < 0:
                neg += 1

    except:
        print("Error tweets: unable to fetch data.")

    # Close the connection
    db.close()

    # calculate the first part of the formula (sum(positive_tweets))/(sum(negative_tweets))
    x = (1+float(pos))/(1+float(neg))
    # and return log(x)
    return math.log(x)




## main program ##
def main():

    #list of days to calculate the sentiment
    days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
            '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
            '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
            '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']

    #read command line arguments (default bing)
    dictionary_name = 'bing'
    if sys.argv[1:]:
        dictionary_name = sys.argv[1]

    # initialize the dictionary d = {}
    dictionary = {}
    #d = retrieve_dictionary('nrc')
    #d = retrieve_dictionary('bing')
    #d = retrieve_dictionary('afinn96')
    #d = retrieve_dictionary('afinn111')
    print dictionary_name
    dictionary = retrieve_dictionary(dictionary_name)

    #dictionary of days with values of sentiment
    #e.g.: {'2016-12-28': 0.1234, '2016-12-29': 0.6789}
    days_sentiment = {}

    #save data on all Sentiment.txt
    out_file = open("Sentiment.txt", "w")

    #for every day, write the calculated sentiment in Sentiment.txt
    for i in range(0, days.__len__()):
        #calculate the sentiment for single day
        days_sentiment[i] = day_sentiment(days[i], dictionary)
        #and write it in Sentiment.txt as "YYYY-MM-DD  0.000"
        out_file.write(days[i] + "   " + str(days_sentiment[i]) + "\n")
        print(days_sentiment[i])
    out_file.close()


    #calculate the matrix dataset
    tollerance = 0.001
    source = "../../datasets/Market_values.txt"
    source_ext = "../../datasets/Market_values_ext.txt"
    source_emission = "Sentiment.txt"
    print("INPUT DATASET:")

    matrix.build_transition_m(matrix.extract(source_ext), tollerance)
    matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance),
                                matrix.delta_emission(matrix.extract(source_emission)))



if __name__ == "__main__":
    main()
