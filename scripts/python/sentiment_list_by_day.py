import MySQLdb
import math

def retrieveVocabulary(vocabular):
        d={}
        # Connect
        db = MySQLdb.connect(host="127.0.0.1",
                             user="root",
                             passwd="password",
                             db="mp - progetto")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        query=""

        if vocabular.__len__() == 1 :
            query= "dictionary = \"" + vocabular[0] + "\";"
        elif vocabular.__len__() == 2 :
            query= "dictionary = \"" + vocabular[0] + "\" or dictionary = \""+ vocabular[1]+ "\" ;"
        elif vocabular.__len__() == 3 :
            query= query + "dictionary = \"" + vocabular[0]+ "\" or dictionary = \""+ vocabular[1] + "\" or dictionary = \""+ vocabular[2]+ "\" ;"
        query="SELECT * FROM dictionary WHERE "+query
        try:
            cursor.execute(query)
            print(query)
            results = cursor.fetchall()
            for row in results:
               w = row[0]
               l = int(row[1])
               d[w] = l

        except:
           print("Error dictionary: unable to fetch data.")

        # Close the connection
        db.close()

        return d

## sentiment(tweet) return a boolean value for the the sentiment of the tweet
def sentiment(tweet,d):
    #sentiment value
    value = 0

    #split in words
    words = tweet.split(' ' )
    #remove non alpha characters
    for i in range (0, words.__len__()):
        words[i] = filter(str.isalpha, words[i])
        if (d.get(words[i]) != None):
            value += int(d.get(words[i]))

    #print(tweet, "->",str(value))
    return value


## day_sentiment(day) return the sentimant of the day
def day_sentiment(day,d):
    #set num and den = 0
    num = 0
    den = 0

    # Connect
    db = MySQLdb.connect(host="127.0.0.1",
                        user="root",
                        passwd="password",
                        db="mp - progetto")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Execute SQL SELECT  statement
    try:
        cursor.execute("SELECT * FROM tweets WHERE tweet_date = \'"+day+"\';")
        results = cursor.fetchall()
        for row in results:
            id_row = int(row[0])
            id_tweet = str(row[1])
            tweet = str(row[2])
            tweet_date = str(row[3])
            sentiment_bool = bool(row[4])

            if sentiment(tweet,d) > 0:
                num += 1
            if sentiment(tweet,d) < 0:
                den += 1

    except:
        print("Error tweets: unable to fetch data.")

    # Close the connection
    db.close()

    x = (1+float(num))/(1+float(den))
    return math.log(x)
