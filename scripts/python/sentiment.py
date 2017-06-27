import MySQLdb
import math


## returns the database vocabulary as python dictionary
## input: vocabulary_request = "bing"
## output: {'love': +2, 'hate': -2, 'abacus': 0, ...}
def retrieveVocabulary(vocabulary_request):
        vocabulary={}
        db = MySQLdb.connect(host="127.0.0.1",
                             user="root",
                             passwd="root",
                             db="experiments")

        # Create and execute SQL query
        cursor = db.cursor()
        query = "SELECT * FROM " + vocabulary_request + ";"
        try:
            cursor.execute(query)
            print(query)
            results = cursor.fetchall()
            # add 'word':'label' in vocabulary for every word in database
            for row in results:
               w = row[0]
               l = int(row[1])
               vocabulary[w] = l

        except:
           print("Error dictionary: unable to fetch data.")
        db.close()

        return vocabulary



## day_sentiment(day) returns the sentimant of the day according to vocab
## input: day = "2016/12/05"
##        vocab = {'love': +2, 'hate': -2, 'abacus': 0, ... }
## output: 0.112
def day_sentiment(day,vocab):
    pos_daySentiment = 0.0
    neg_daySentiment = 0.0

    db = MySQLdb.connect(host="127.0.0.1",
                        user="root",
                        passwd="root",
                        db="experiments")

    # Create and execute SQL query
    cursor = db.cursor()
    query = "SELECT tweet FROM tweets WHERE tweet_date = \'" + day + "\';"
    try:
        cursor.execute(query)
        print(query)
        results = cursor.fetchall()
        for row in results:
            tweet = str(row[0])
            score = sentiment(tweet,vocab)  # sentiment of single tweet
            if score > 0:
                pos_daySentiment += 1
            elif score < 0:
                neg_daySentiment+= 1
    except:
        print("Error tweets: unable to fetch data.")
    db.close()

    # calculate sentiment with simple sentiment logit scale sentiment formula
    daySentiment = (1 + pos_daySentiment) / (1 + neg_daySentiment)
    
    return math.log(daySentiment)



## returns the sentiment of the tweet according to vocab
## input: tweet = "love love love hate #xyz" 
##        vocab = {'love': +2, 'hate': -2, ... }
## output: 4.0
def sentiment(tweet,vocab):
    score = 0.0            
    words = tweet.split(' ' )  #split in words

    #remove non alpha characters
    for i in range (0, words.__len__()):
        words[i] = filter(str.isalpha, words[i])
        if (vocab.get(words[i]) != None):
            score += int(vocab.get(words[i]))
    return score

