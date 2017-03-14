from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml

# Load config file
if file("/vagrant/tweetled_config.yaml", "r"):
    cfg_file_path = file("/vagrant/tweetled_config.yaml", "r")
elif file("./tweetled_config.yaml", "r"):
    cfg_file_path = file("./tweetled_config.yaml", "r")

if cfg_file:
    cfg_file = yaml.load(cfg_file_path)
else:
    print "No config file found."

consumer_key = cfg_file['consumer_key']
consumer_secret = cfg_file['consumer_secret']

access_token = cfg_file['access_token']
access_token_secret = cfg_file['access_token_secret']

class listener(StreamListener):

    def on_data(self, data):
        print(data)
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