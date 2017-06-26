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




def main():
    tweets_file = "example.json"

    with open(tweets_file, 'rU') as lines:
        for line in lines:
            tweet_text = extractText(line)
            tweet_date = extractDate(line)

            if tweet_text != 0:
                print(tweet_text)
                print(tweet_date)
                # and do things like insert in database


if __name__ == "__main__":
    main()
