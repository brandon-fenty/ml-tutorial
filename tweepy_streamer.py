from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import twitter_credentials
import numpy as np
import pandas as pd
# This application was coded by following  the "Tweet Visualization and Sentiment Analysis in Python Tutorial"
# from Vincent Russo of Lucid Programming


class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuth().authenticate_twitter()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets_list = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets_list.append(tweet)
        return tweets_list


class TwitterAuth:
    @staticmethod
    def authenticate_twitter():
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
        if status == 420:
            # Terminate connection if twitter rate limit is exceeded
            return False
        print(status)


class TweetAnalyzer:
    """
    Used to analyze tweet data and categorize it
    """
    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['favorites'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    df = tweet_analyzer.tweets_to_df(tweets)
    # print("Average likes - ", np.mean(df['favorites']))
    # print("Most likes - ", np.max(df['favorites']))
    # print(dir(tweets[0]))
    print(df.head(20))
    # print(tweets[0].in_reply_to_screen_name)
