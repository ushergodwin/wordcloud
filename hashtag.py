__author__ = "Tumuhimbise Godwin"
__copyright__ = "Copyright 2021, Trending Hashtags Project"
__credits__ = ["Ojok David"]
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Tumuhimbise Godwin"
__email__ = "godwintumuhimbise96@gmail.com"
__status__ = "Production"
try:
    import tweepy
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import requests
    import base64
    import json
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ImportError:
    raise ImportError('Failed to import the tkinter package')

root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=500)
canvas1.pack()


class TwitterHashtags:
    __USER_KEY = None
    __USER_SECRET = None
    __ACCESS_TOKEN = None
    __ACCESS_TOKEN_SECRET = None
    __b64_encoded_key = None
    __access_token = None
    __region = None
    __auth = False

    def __init__(self):
        self.__auth = True

    @classmethod
    def userKey(cls, api_key: str):
        """
        :param api_key Your App API KEY
        :return str API KEY
        """
        cls.__USER_KEY = api_key
        return cls.__USER_KEY

    @classmethod
    def userSecret(cls, secret_key: str):
        """
        :param secret_key Your APP PAI SECRET KEY
        :return str SECRETE KEY
        """
        cls.__USER_SECRET = secret_key
        return cls.__USER_SECRET

    @classmethod
    def accessToken(cls, access_token: str):
        """
        :param access_token The access token for your App
        :return str
        """
        cls.__ACCESS_TOKEN = access_token
        return cls.__ACCESS_TOKEN

    @classmethod
    def secretAccessToken(cls, secret_access_token: str):
        """
        :param secret_access_token The secret access token for your app
        :return str
        """
        cls.__ACCESS_TOKEN_SECRET = secret_access_token
        return cls.__ACCESS_TOKEN_SECRET

    @classmethod
    def region(cls, region: int):
        """
        :param region The WOEID code representing your region of interest, eg 1 for the word
        Visit https://nations24.com/world-wide for more details
        :return int
        """
        cls.__region = region
        return cls.__region

    @classmethod
    def beginProcess(cls):
        global root
        """
        initiates the process
        """
        cls.__authKeys()
        labelConfig("authenticating \n", True)
        cls.__authResponse()
        labelConfig("200 done \n", True)
        labelConfig("sending request for hashtags \n", True)
        labelConfig("200 done \n", True)
        labelConfig("printing the word cloud", True)

    @classmethod
    def __authKeys(cls):
        """
        Sets the API keys for use in the requests
        """
        # Reformat the keys and encode them
        key_secret = '{}:{}'.format(cls.__USER_KEY, cls.__USER_SECRET).encode('ascii')
        # Transform from bytes to bytes that can be printed
        cls.__b64_encoded_key = base64.b64encode(key_secret)
        # Transform from bytes back into Unicode
        cls.__b64_encoded_key = cls.__b64_encoded_key.decode('ascii')
        return key_secret

    @classmethod
    def __authUrl(cls):
        """
        Sets the url to be used in requests
        :return str url
        """
        base_url = 'https://api.twitter.com/'
        return '{}oauth2/token'.format(base_url)

    @classmethod
    def __authHeaders(cls):
        """
        Sets the headers to parse along with the request
        :return dict
        """
        return {
            'Authorization': 'Basic {}'.format(cls.__b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

    @classmethod
    def __authData(cls):
        """
        Sets the type of auth to use
        :return dict
        """
        return {
            'grant_type': 'client_credentials'
        }

    @classmethod
    def __authResponse(cls):
        """
        Performs the request
        :returns int Response code
        """
        auth_resp = requests.post(cls.__authUrl(), headers=cls.__authHeaders(), data=cls.__authData())
        cls.__access_token = auth_resp
        return auth_resp

    @classmethod
    def __accessToken(cls):
        """
        Returns the access token to use when making the request for hashtags
        """
        return cls.__access_token.json()['access_token']

    @classmethod
    def __trendHeaders(cls):
        """
        Sets the headers to use when fetching hashtags
        :return dict
        """
        return {
            'Authorization': 'Bearer {}'.format(cls.__accessToken())
        }

    @classmethod
    def __trendsParam(cls):
        """
        Sets the region where to get the trends from
        ID in form of WOEID codes
        :return dict
        """
        return {
            'id': cls.__region,
        }

    @classmethod
    def __sendRequest(cls):
        """
        Makes a request for the hashtags
        Returns a list with top 50 trending hashtags
        :return list
        """
        trend_url = 'https://api.twitter.com/1.1/trends/place.json'
        trend_resp = requests.get(trend_url, headers=cls.__trendHeaders(), params=cls.__trendsParam())
        return trend_resp.json()

    @classmethod
    def __getHashtags(cls):
        """
        Returns hashtags in a text format to be used for making a word cloud
        :return str
        """
        tweet_data = cls.__sendRequest()
        return "".join("#" + tweet_data[0]['trends'][i]['name'] for i in range(50))

    @classmethod
    def formWordCloud(cls):
        """
        Plots the graph and forms a word cloud
        """
        hashtags = cls.__getHashtags()
        word_cloud = WordCloud().generate(hashtags)
        plt.figure(figsize=(12, 6))
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()


def Config():
    # parse your APP's API KEY
    TwitterHashtags.userKey("qIxgmf1iaij1zLcZGBp21QTDR")

    # parse your APP's SECRET KEY
    TwitterHashtags.userSecret("XZnXIyFcDbweDlN3A4irHao9ChHLETr0UjgJKkFg4hZeVW06Uj")

    # parse your APP's Access Token
    TwitterHashtags.accessToken("1381352137750364172-I1Sbgmc2uQS33Y0dyYoC6mqOtYC3eu")

    # parse your APP's Secret Access Token
    TwitterHashtags.secretAccessToken("WbxkNcKUKBwGquasks4OBbRzH4nPDAvRwu6YXpydgsCgZ")

    # set the region to pick the hashtags from
    TwitterHashtags.region(23424863)

    # Begin the process
    TwitterHashtags.beginProcess()

    # Draw a word cloud
    TwitterHashtags.formWordCloud()


label = tk.Label(root, text='TRENDING HASHTAGS WORD WIDE \n')
label.config(font=('Arial', 18))
canvas1.create_window(300, 50, window=label)


def labelConfig(string, append=False):
    if append:
        text = label.cget("text") + string
        label.configure(text=text)
    else:
        label.configure(text=string)


def runsetup():
    labelConfig("getting things ready \n", True)
    Config()


button2 = tk.Button(root, text='CLICK TO GET TOP 50 HASHTAGS', command=runsetup, bg='green', fg='white')
canvas1.create_window(150, 150, window=button2)
root.mainloop()
