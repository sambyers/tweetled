from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml

# Load config file
cfg_file = yaml.load("/vagrant/tweetled_config.yaml")
print cfg_file