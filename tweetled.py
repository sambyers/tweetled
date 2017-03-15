from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml
import os
import json

# Load config file
if os.path.exists("/vagrant/tweetled_config.yaml"):
    cfg_file = file("/vagrant/tweetled_config.yaml", "r")
elif os.path.exists("tweetled_config.yaml"):
    cfg_file = file("tweetled_config.yaml", "r")
else:
    cfg_file = None

if cfg_file:
    cfg_file = yaml.load(cfg_file)
else:
    print "No config file found."

consumer_key = cfg_file['consumer_key']
consumer_secret = cfg_file['consumer_secret']

access_token = cfg_file['access_token']
access_token_secret = cfg_file['access_token_secret']

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

class listener(StreamListener):
    byteify = json_loads_byteified
    def on_data(self, data):
        data = byteify(data)
        # text = data['text']
        # screen_name = data['screen_name']
        # print screen_name + " tweeted: " + text
        print type(data)
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