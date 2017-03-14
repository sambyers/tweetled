from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml

# Load config file
cfg_file_path = file("/vagrant/tweetled_config.yaml", "r")
cfg_file = yaml.load(cfg_file_path)
print cfg_file