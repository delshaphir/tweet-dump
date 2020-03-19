# Tweet Dump

Gets all of a given user's original (non-retweet, non-reply) tweets since the beginning of time. Use at your own risk.

## Get it

Clone this repo:

```bash
git clone git@github.com:jedfras/tweet-dump.git
```

## Usage

```bash
python tweet_dump.py [screen_name]
```

## What does it do?
Tweet Dump will make a text file (`screen_name.txt`) containing the text of all of the given user's original tweets.
If a tweet contains line breaks, they will be removed.

