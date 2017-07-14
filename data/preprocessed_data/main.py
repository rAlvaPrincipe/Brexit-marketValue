import sys
import collections


def retrieve_market(market_file):
    lines = open(market_file).read().split("\n")
    market = {}

    for line in lines:
        if line != "":
            line = line.split("\t")
            date = line[0]
            value = line[1]
            market[date] = value

    return market

def retrieve_sentiment(sentiment_file):
    lines = open(sentiment_file).read().split("\n")
    sentiment = {}

    for line in lines:
        if line != "":
            line = line.split("\t")
            date = line[0]
            value = line[1]
            sentiment[date] = value

    return sentiment

def retrieve_tweets_per_day(tweets_per_day_file):
    lines = open(tweets_per_day_file).read().split("\n")
    tweets_per_day = {}

    for line in lines:
        if line != "":
            line = line.split("\t")
            date = line[0]
            value = line[1]
            tweets_per_day[date] = value

    return tweets_per_day

def main():
    #save data
    vocabulary = ["afinn96", "afinn111", "bing", "nrc", "afinn_bing_base_bing", "afinn_bing_base_afinn"]
    markets = ["ecb.europa.eu", "exchangerates.com", "investing.com", "ofx.com", "pundsterlinglive.com"]

    for v in vocabulary:
        for m in markets:
            # MARKET
            market_file = "./markets/market_from_"+ m +".txt"
            market = retrieve_market(market_file)
            # SENTIMENT
            sentiment_file = "./sentiments/w999_"+ v +"_tweets.txt"
            sentiment = retrieve_sentiment(sentiment_file)
            # TWEETS PER DAY
            tweets_per_day_file = "./days_count.txt"
            tweets_per_day = retrieve_tweets_per_day(tweets_per_day_file)

            # find days with sentiment AND market AND tweets_per_day > 1000
            new_market = {}
            new_sentiment = {}
            for day in market:
                condition = day in sentiment and day in tweets_per_day
                condition = condition and float(sentiment[day]) != 0.0 and int(tweets_per_day[day]) > 1000
                if condition:
                    new_market[day] = market[day]
                    new_sentiment[day] = sentiment[day]

            #check if something gone wrong
            if len(new_market) != len(new_sentiment):
                raise ValueError('error in new market and sentiment length!')
                return -1

            #order data
            new_sentiment = collections.OrderedDict(sorted(new_sentiment.items()))
            new_market = collections.OrderedDict(sorted(new_market.items()))

            #write new sentiment
            outputSentiment = open("./output/output_sentiment_"+ v +"_market_from_"+ m +".txt", "w")
            for day in new_sentiment:
                outputSentiment.write(str(day)+"\t"+str(new_sentiment[day])+ "\n")
            outputSentiment.close()
            #write new markets
            outputMarket = open("./output/output_market_"+ v +"_market_from_"+ m +".txt", "w")
            for day in new_market:
                outputMarket.write(str(day)+"\t"+str(new_market[day])+ "\n")
            outputMarket.close()


if __name__ == "__main__":
    main()
