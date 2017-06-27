import json

#extract the text from tweet json file
def extractText(json_data):
    parsed_json = json.loads(json_data)
    #return tweet text
    if 'title' in parsed_json:
        return parsed_json['title']
    elif 'text' in parsed_json:
        return parsed_json['text']
    else:
        return 0

#extract the date from tweet json file
def extractDate(json_data):
    parsed_json = json.loads(json_data)
    #return tweet date
    if 'date' in parsed_json:
        yy_mm_dd = parsed_json['date'][0:10]
        return yy_mm_dd
    else:
        return 0

# remove non ascii characters from string
def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)


# main
def main():
    tweet_sql_file = "tweets_resolved_brexit.sql"
    # add the creation table at start
    f = open(tweet_sql_file, 'a')
    table_creation = """USE experiments;
    CREATE TABLE IF NOT EXISTS tweets_resolved_brexit(
        id INT UNSIGNED NOT NULL,
        tweet varchar(255) NOT NULL,
        tweet_date DATE NOT NULL,
        PRIMARY KEY (id),
        INDEX tweet_date (tweet_date)
    );

    """
    f.write(table_creation)
    f.close

    # tweets json
    tweets_file = "resolved_brexit.json"
    counter = 0

    f = open(tweet_sql_file, 'a')

    # read line by line (rU heps because read one line at time)
    with open(tweets_file, 'rU') as lines:
        for line in lines:
            tweet_text = extractText(line)
            tweet_date = extractDate(line)

            if tweet_text != 0 and tweet_text is not None:
                tweet_text = _removeNonAscii(tweet_text)
                tweet_text = str(tweet_text).replace("'", "\\'")
                counter += 1
                query = "INSERT INTO tweets_resolved_brexit VALUES (\'"+str(counter)+"\',\'"+tweet_text+"\',\'"+str(tweet_date)+"\');\n"
                f.write(query)

    f.close


if __name__ == "__main__":
    main()
