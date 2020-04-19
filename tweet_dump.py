import sys
import requests
import secret_stuff as ss

sys.path.append('/home/jedfr/.local/lib/python2.7/site-packages/')
import requests_oauthlib
import twitter

import csv

def main():
    # Initialize api
    api = twitter.Api(consumer_key=ss.CONSUMER_KEY,
        consumer_secret=ss.CONSUMER_SECRET,
        access_token_key=ss.TOKEN,
        access_token_secret=ss.SECRET)

    screen_name = sys.argv[1]
    screen_names = ['thetalkingjed', 'isnascarasport', 'wildenian_thot']
    FILENAME = screen_name + '.csv'

    # Overrwite current file first
    with open(file=FILENAME, mode='w') as f:
        f.write('')

    # Get statuses
    COUNT = 200
    statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=COUNT)
    last_id = 0
    while len(statuses) > 0:
        with open(file=FILENAME, mode='a') as csvfile:
            writer = csv.writer(csvfile)
            for s in statuses:
                writer.writerow([s.text.replace('\n', ''), screen_name])
                last_id = s.id
        statuses = api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True, count=COUNT, max_id=last_id - 1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python {0} [screen_name]'.format(sys.argv[0]))
        sys.exit()
    main()