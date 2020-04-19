import sys
import requests
import secret_stuff as ss

sys.path.append('/home/jedfr/.local/lib/python2.7/site-packages/')
import requests_oauthlib
import twitter
import string
import pprint as pp
import csv
from typing import List
import random

class TweetDataGatherer:

    def __init__(self, api: twitter.Api, screen_names: List[str], count=200):
        self.api = api 
        self.screen_names = screen_names
        self.count = count

    def prepare_text(self, text: str):
        return text.replace('\n', ' ')

    def case_ratio(self, text: str):
        upper_count = sum([1.0 for c in text if c.isupper()])
        return upper_count / len(text)

    def punctuation_count(self, text: str):
        return sum([1 for c in text if c in string.punctuation])

    """
    def emoji_count(self, text:str):
        return sum([1 for c in text if c in emoji.UNICODE_EMOJI])
    """

    """
    DATA COLUMNS
    * text: raw text of tweet (line breaks removed)
    * length: character count of tweet
    * case value: percentage of uppercase characters in text
    * punctuation count: number of punctuation characters in text
    """

    def collect_data(self):
        '''
        Returns a dictionry mapping authors to lists of their tweet data (as described above)
        '''
        data_per_author = {}
        for screen_name in self.screen_names:
            statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=self.count)
            last_id = 0
            while len(statuses) > 0:
                for s in statuses:
                    text, author = s.full_text, s.user.screen_name.lower()
                    row = [self.prepare_text(text), len(text), self.case_ratio(text), self.punctuation_count(text)]
                    if author in data_per_author:
                        data_per_author[author].append(row)
                    else:
                        data_per_author[author] = [row]
                    last_id = s.id
                statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=self.count, max_id=last_id - 1)
        return data_per_author

# Initialize Twitter api
api = twitter.Api(consumer_key=ss.CONSUMER_KEY,
    consumer_secret=ss.CONSUMER_SECRET,
    access_token_key=ss.TOKEN,
    access_token_secret=ss.SECRET,
    tweet_mode='extended')

# Get all tweets from each user
gatherer = TweetDataGatherer(api=api, screen_names=['thetalkingjed', 'isnascarasport', 'wildenian_thot'])
all_per_user = gatherer.collect_data()

# Randomly sample 250 from each user
training_per_user = {}
training_list = []
validation_list = []
sample_size = 250
for key in all_per_user.keys():
    data = all_per_user[key]
    training_per_user[key] = random.sample(data, sample_size)

# Randomly sample validation data (50 from each user) and build lists
for key in training_per_user.keys():
    data = training_per_user[key]
    random.shuffle(data)
    removed = [data.pop() for _ in range(50)]
    training_list.extend([(entry + [key]) for entry in data])
    validation_list.extend([(entry + [key]) for entry in removed])

# Shuffle all training and validation data
random.shuffle(training_list)
random.shuffle(validation_list)

# Write to .csv files
training_file = 'training.csv'
validation_file = 'validation.csv'

with open(training_file, mode='w') as csvfile:
    writer = csv.writer(csvfile)
    for data in training_list:
        writer.writerow(data)

with open(validation_file, mode='w') as csvfile:
    writer = csv.writer(csvfile)
    for data in validation_list:
        writer.writerow(data)