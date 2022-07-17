from twython import Twython
import json
import time
import pandas as pd
from yaml import load

LANGUAGE = 'fa'
TWEET_PER_SEARCH_NUMBER = 50
API_CALL_INTERVAL = 5


def load_credentials():
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)
        return creds


def init_twython_access():
    creds = load_credentials()
    twython = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    return twython


def read_keywords_from_file(file_name):
    key_words = []
    with open(file_name) as txtFile:
        lines = txtFile.readlines()
        for line in lines:
            key_words.extend(line.split(","))

    print("We have ", len(key_words), " keywords.")
    return key_words


def append_query_to_dict(query_results, data_dict):
    for status in query_results['statuses']:
        data_dict['user'].append(status['user']['screen_name'])
        data_dict['date'].append(status['created_at'])
        data_dict['text'].append(status['text'])
        data_dict['favorite_count'].append(status['favorite_count'])


def search_for_single_keyword(word, twython_access, data_dict):
    query = {'q': word.strip(),
             'result_type': 'recent',
             'count': TWEET_PER_SEARCH_NUMBER,
             'lang': LANGUAGE,
             }
    query_results = twython_access.search(**query)
    print("Got ", len(query_results['statuses']),
          "tweets for: ", word.strip())
    append_query_to_dict(query_results, data_dict)


def search_for_keywords(key_words, twython_access, data_dict):
    for word in key_words:
        search_for_single_keyword(word, twython_access, data_dict)
        time.sleep(API_CALL_INTERVAL)
    return data_dict


def data_dict_to_csv(data_dict):
    df = pd.DataFrame(data_dict)
    df.to_csv('data.csv')
    print(df.shape)


def main():
    data_dict = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
    twython_access = init_twython_access()
    key_words = read_keywords_from_file('keywords.txt')
    search_for_keywords(key_words, twython_access, data_dict)
    data_dict_to_csv(data_dict)


if __name__ == "__main__":
    main()
