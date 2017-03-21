from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml
import os
import sys
import json
import time
import argparse
from rgbmatrix import RGBMatrix, RGBMatrixOptions

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

def random_color():
        color = random.randrange(0, 255)
        return color


def run_led_text(my_text):

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 16
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("/fonts/7x13.bdf")
    textColor = graphics.Color(random_color(), random_color(), random_color())
    pos = offscreen_canvas.width
    print my_text

    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        text = data['text']
        screen_name = data['user']['screen_name']
        msg = screen_name + " tweeted: " + text
        print msg
        run_text = run_led_text(msg)
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