from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml
import os
import sys
import json

# Load config file
if os.path.exists("/vagrant/tweetled_config.yaml"):
    cfg_file = file("/vagrant/tweetled_config.yaml", "r")
elif os.path.exists("tweetled_config.yaml"):
    cfg_file = file("tweetled_config.yaml", "r")
else:
    cfg_file = False

if cfg_file:
    cfg_file = yaml.load(cfg_file)
else:
    print "No config file found."
    sys.exit()

consumer_key = cfg_file['consumer_key']
consumer_secret = cfg_file['consumer_secret']

access_token = cfg_file['access_token']
access_token_secret = cfg_file['access_token_secret']

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        text = data['text']
        screen_name = data['user']['screen_name']
        print screen_name + " tweeted: " + text
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = listener()
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    except:
        print "Authentication failed."

    stream = Stream(auth, l)
    stream.filter(track=['#devnetroanoke'])