import HTMLParser
import json
import os
import nltk
import random
import time

from urllib2 import urlopen
#from pokemon_names import names

def abs_path(rel_path):
	""" Gets absolute path of this current file,
		grab its directory, append to relative path
		to return absolute path. """

	my_path = os.path.abspath(__file__)
	my_dir = os.path.dirname(my_path)
	return os.path.join(my_dir, rel_path)

def get_quotesondesign():
    json_quotesondesign = "http://quotesondesign.com/api/3.0/api-3.0.json"
    response = urlopen(json_quotesondesign).read()
    results_dict = json.loads(response)
    if results_dict:
        quote_selected = (HTMLParser.HTMLParser().unescape(results_dict['quote'].rstrip()), HTMLParser.HTMLParser().unescape(results_dict['author']))
    print quote_selected
    return quote_selected

def create_wisdom():

	# open pokemon json file
	f = open(abs_path("pokemons.json"), "r")
	all_pokemons_dicts = json.load(f)
	f.close()

	# Choose a random Pokemon index number
	pokemon_index = random.randint(0, len(all_pokemons_dicts))
	pokemon_selected = all_pokemons_dicts[pokemon_index]
	pokemon_name = pokemon_selected["name"]
	pic_file = open(abs_path(pokemon_selected["pic_path"]), "rb")

	#Get quote from API
	quote_selected = get_quotesondesign()
	text = nltk.word_tokenize(quote_selected[0])

	#Find a random noun in the quote
	noun_tags = ["NN","NNS","NNP","NNPS","PRP"]
	quote_split = nltk.pos_tag(text)

	nouns = [word for word, part in quote_split if part in noun_tags]

	noun_to_replace = random.choice(nouns) #need to take out repeats

	quote_selected = (quote_selected[0].replace(noun_to_replace,pokemon_name), quote_selected[1])

	tweet = quote_selected[0] + " -" + quote_selected[1] + " #PokemonGo"
	print len(tweet)

	if len(tweet) <= 140:
		return tweet, pic_file
	else:
		minutes = 10
		time.sleep(minutes*60)
		create_wisdom()

print create_wisdom()