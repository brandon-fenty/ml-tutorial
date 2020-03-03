from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import twitter_credentials
# This application was coded by following  the "Tweet Visualization and Sentiment Analysis in Python Tutorial"
# from Vincent Russo of Lucid Programming


class TwitterAuth:

    def authenticate_twitter(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer:
    """
    A class to stream and process live tweets
    """
    def __init__(self):
        self.twitter_auth = TwitterAuth()

    def stream_tweets(self, fetched_tweets_file, hash_tags):
        # Handles connecting to and streaming tweets from the Twitter API
        listener = TwitterListener(fetched_tweets_file)
        auth = self.twitter_auth.authenticate_twitter()

        stream = Stream(auth, listener)
        stream.filter(track=hash_tags)


class TwitterListener(StreamListener):
    """
    Basic listener class that prints data from the Twitter stream to stdOut
    """
    def __init__(self, fetched_tweets_file):
        self.fetched_tweets_file = fetched_tweets_file

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_file, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == "__main__":

    hash_tags = ["libertymutual", "limu", "safeco", "insurance"]
    fetched_tweets_file = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_file, hash_tags)
