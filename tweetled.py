from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml

# Load config file
cfg_file_path = file("/vagrant/tweetled_config.yaml", "r")
cfg_file = yaml.load(cfg_file_path)

consumer_key = cfg_file['consumer_key']
consumer_secret = cfg_file['consumer_secret']

access_token = cfg_file['access_token']
access_token_secret = cfg_file['access_token_secret']

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['devnetroanoke'])