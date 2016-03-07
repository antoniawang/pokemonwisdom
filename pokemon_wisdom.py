import HTMLParser
import json
import nltk
import random
import time

from urllib2 import urlopen
from pokemon_names import names

def get_quotesondesign():
        json_quotesondesign = "http://quotesondesign.com/api/3.0/api-3.0.json"
        response = urlopen(json_quotesondesign).read()
        results_dict = json.loads(response)
        if results_dict:
            quote_selected = (HTMLParser.HTMLParser().unescape(results_dict['quote'].rstrip()), HTMLParser.HTMLParser().unescape(results_dict['author']))
        print quote_selected
        return quote_selected

def create_wisdom():

	#Choose a random Pokemon index number
	pokemon_index = random.randint(0, len(names))

	pokemon_selected = names[pokemon_index]


	#Get quote from API
	quote_selected = get_quotesondesign()
	text = nltk.word_tokenize(quote_selected[0])

	#Find a random noun in the quote
	noun_tags = ["NN","NNS","NNP","NNPS","PRP"]
	quote_split = nltk.pos_tag(text)

	nouns = [word for word, part in quote_split if part in noun_tags]

	noun_to_replace = random.choice(nouns) #need to take out repeats

	quote_selected = (quote_selected[0].replace(noun_to_replace,pokemon_selected), quote_selected[1])

	tweet = quote_selected[0] + " -" + quote_selected[1] + " #pokemon #wisdom"

	if len(tweet) <= 140:
		return tweet
	else:
		minutes = 10
		time.sleep(minutes*60)
		create_wisdom()

print create_wisdom()