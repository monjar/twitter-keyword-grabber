from twython import Twython
import json
import time
import pandas as pd

LANGUAGE = 'fa'
TWEET_PER_SEARCH_NUMBER = 50
API_CALL_INTERVAL = 5

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

keyWords = []
with open('keywords.txt') as txtFile:
    lines = txtFile.readlines()
    for line in lines:
        keyWords.extend(line.split(","))

print("We have ", len(keyWords), " keywords.")

dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
try:
    for word in keyWords:
        print("Getting \"", word, "\" Tweets...")
        query = {'q': word.strip(),
            'result_type': 'recent',
            'count': TWEET_PER_SEARCH_NUMBER,
            'lang': LANGUAGE,
        }
        queryResults = python_tweets.search(**query)
        print("Got ", len(queryResults['statuses']), "tweets for: ", word.strip())
        for status in queryResults['statuses']:
            dict_['user'].append(status['user']['screen_name'])
            dict_['date'].append(status['created_at'])
            dict_['text'].append(status['text'])
            dict_['favorite_count'].append(status['favorite_count'])
        time.sleep(API_CALL_INTERVAL)
except:
    print("Something went wrong...")

df = pd.DataFrame(dict_)
df.to_csv('data.csv') 
print(df.shape)