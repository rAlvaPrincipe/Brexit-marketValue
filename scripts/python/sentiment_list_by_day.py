import MySQLdb
import math

## retrieveVocabulary(vocabulary_name) return the database vocabulary as python dictionary
## eg: retrieveVocabulary(bing) -> {'love':+2, 'hate': -2, 'abacus': 0}
def retrieveVocabulary(vocabulary_request):
        vocabulary={}
        db = MySQLdb.connect(host="127.0.0.1",
                             user="root",
                             passwd="root",
                             db="experiments")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        query = "SELECT word, label FROM " + vocabulary_request + ";"
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


## sentiment(tweet) return a value for the the sentiment of the tweet
## eg: sentiment('love love love hate #xyz', {'love':+2, 'hate': -2}) -> 4
def sentiment(tweet,vocab):
    score = 0                  #sentiment value
    words = tweet.split(' ' )  #split in words

    #remove non alpha characters
    for i in range (0, words.__len__()):
        words[i] = filter(str.isalpha, words[i])
        if (vocab.get(words[i]) != None):
            score += int(vocab.get(words[i]))
    return score


## day_sentiment(day) return the sentimant of the day
def day_sentiment(day,vocab):
    pos_daySentiment = 0
    neg_daySentiment = 0

    db = MySQLdb.connect(host="127.0.0.1",
                        user="root",
                        passwd="root",
                        db="experiments")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    query = "SELECT tweet FROM tweets WHERE tweet_date = \'" + day + "\';"
    # Execute SQL SELECT  statement
    try:
        cursor.execute(query)
        print(query)
        results = cursor.fetchall()
        for row in results:
            tweet = str(row[0])
            # calculate the sentiment of single tweet
            score = sentiment(tweet,vocab)
            if score > 0:
                pos_daySentiment += 1
            elif score < 0:
                neg_daySentiment+= 1
    except:
        print("Error tweets: unable to fetch data.")

    db.close()
    # calculate sentiment with simple sentiment logit scale sentiment formula
    # sentiment = log(sum(positive) / sum(negative))
    daySentiment = float( 1 + pos_daySentiment ) / float( 1 + neg_daySentiment )
    
    return math.log(daySentiment)
