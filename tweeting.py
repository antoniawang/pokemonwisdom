import os, time, sys
import twitter
from pokemon_wisdom import create_wisdom

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

#check if credentials are correct
print api.VerifyCredentials()

#send a tweet every 24 hours
status, pic_file = create_wisdom()
print status

# when media no longer counts towards 140 characters, add media=pic_file option
api.PostUpdate(status=status)

pic_file.close()