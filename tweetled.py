from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from ..rpi-rgb-led-matrix.python.samples.samplebase import SampleBase
from ..rpi-rgb-led-matrix.python.rgbmatrix import graphics
import yaml
import os
import sys
import json
import time

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

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/fonts/7x13.bdf")
        textColor = graphics.Color(random_color(), random_color(), random_color())
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        text = data['text']
        screen_name = data['user']['screen_name']
        #print screen_name + " tweeted: " + text
        run_text = RunText(my_text=screen_name + " tweeted: " + text)
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