from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from yaml import load

# Load config file
cfg_file = load("/vagrant/tweetled_config.yaml")
print cfg_file