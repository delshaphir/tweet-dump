# Tweet Dump

Gets all of a given user's original (non-retweet, non-reply) tweets since the beginning of time. Use at your own risk.

## Get it

Clone this repo:

```bash
git clone git@github.com:jedfras/tweet-dump.git
```

## Usage

Making requests from the Twitter API requires using authorization tokens and secrets, which are referred to from a file called secret_stuff.

Follow the instructions [here](https://python-twitter.readthedocs.io/en/latest/getting_started.html) to make a Twitter App and get those tokens and whatnot.

After you've cloned this repo, create a file in its root folder called `secret_stuff.py` with the right information, like so:

```
CONSUMER_KEY = '[consumer api key goes here]'
CONSUMER_SECRET = '[consumer api secret goes here]'
TOKEN = '[access token goes here]'
SECRET = '[access token secret goes here]'
```

Now, you should be ready to go. Run from the command line like so:

```
python tweet_dump.py [screen_name]
```

## What does it do?
Tweet Dump will make a text file (`screen_name.txt`) containing the text of all of the given user's original tweets.
If a tweet contains line breaks, they will be removed.

## How is it made?

Using **python-twitter**

* Read the [docs](https://python-twitter.readthedocs.io/en/latest/) 
* View the [GitHub](https://github.com/bear/python-twitter)

