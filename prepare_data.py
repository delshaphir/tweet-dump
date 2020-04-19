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
    * emoji value: number of emoji in text
    """

    def collect_data(self, filename: str):
        data = []
        for screen_name in self.screen_names:
            statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=self.count)
            last_id = 0
            with open(file=filename, mode='a') as csvfile:
                writer = csv.writer(csvfile)
                while len(statuses) > 0:
                    for s in statuses:
                        text, author = s.full_text, s.user.screen_name
                        row = [self.prepare_text(text), len(text), self.case_ratio(text), self.punctuation_count(text), author]
                        writer.writerow(row)
                        data.append(row)
                        last_id = s.id
                    statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=self.count, max_id=last_id - 1)
        return data

# Initialize Twitter api
api = twitter.Api(consumer_key=ss.CONSUMER_KEY,
    consumer_secret=ss.CONSUMER_SECRET,
    access_token_key=ss.TOKEN,
    access_token_secret=ss.SECRET,
    tweet_mode='extended')

# Overrwite current file first
filename = 'tweet_data.csv'
with open(file=filename, mode='w') as f:
    f.write('')

# Gather data
gatherer = TweetDataGatherer(api=api, screen_names=['thetalkingjed', 'isnascarasport', 'Wildenian_Thot'])
data = gatherer.collect_data(filename)
pp.pprint(data)