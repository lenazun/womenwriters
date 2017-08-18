import json
import requests
from TwitterAPI import TwitterAPI
import random
import urllib
from datetime import datetime
import os


api = TwitterAPI(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                 consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                 access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
				access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

def get_data():

    #read the data on the json file
    with open('WomenWriters.json') as data_file:
        writers = json.load(data_file)

    #choose one at random
    writer = random.choice(writers)

    return writer


def make_tweet(writer):

    #download the image to disk
    try:
        urllib.urlretrieve(writer['image'], 'temp.jpg')
        image = True
    except:
        image = False

    #try some of the optional items on the data
    try:
        date_of_birth = datetime.strptime(writer['date_of_birth'][:10], '%Y-%m-%d')
        date_of_birth = "(" + date_of_birth.strftime('%Y') + ")"
    except:
        date_of_birth = ""

    try:
        Twitter_username = "@" + writer['Twitter_username']
    except:
        Twitter_username = ""

    #make a nice tweet text TODO make decisions based on char count
    tweet = [("%s%s %s. %s %s") % (writer['womenLabel'], Twitter_username, date_of_birth,
                             writer['womenDescription'],
                             writer['article']), image]

    return tweet


def send(tweet):

    text, image = tweet

    #upload the image
    if image:
        file = open('temp.jpg', 'rb')
        data = file.read()
        r = api.request('media/upload', None, {'media': data})
    
        if r.status_code == 200:
            media_id = r.json()['media_id']
    else:
        media_id = ""

    r = api.request('statuses/update', {'status':text, 'media_ids':media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')

def main():
    send(make_tweet(get_data()))


if __name__ == '__main__':
    main()
