import json
import nltk
import random
from quotes import raw_quotes
from pokemon_names import names

#Choose a random Pokemon index number
pokemon_index = random.randint(0, len(names))

pokemon_selected = names[pokemon_index]



#Turn raw quotes into a list of tuples (quote, author)
quotes = []

for i in range(0, len(raw_quotes), 2):
	quotes.append((raw_quotes[i],raw_quotes[i+1]))


#Choose a random quote
quote_selected = random.choice(quotes)
text = nltk.word_tokenize(quote_selected[0])

#Find a random noun in the quote
noun_tags = ["NN","NNS","NNP","NNPS","PRP"]
quote_split = nltk.pos_tag(text)

nouns = [word for word, part in quote_split if part in noun_tags]

noun_to_replace = random.choice(nouns) #need to take out repeats


quote_selected = (quote_selected[0].replace(noun_to_replace,pokemon_selected), quote_selected[1])


tweet = quote_selected[0] + " " + quote_selected[1] + " #pokemon #wisdom"

print tweet

#turn tweet into dictionary to jsonify
tweet_dict = {"tweet":tweet,
			  "okay": False,
			  "tweeted_on": None
			  }

#jsonifying
with open("tweets.json", "r") as fp:
	tweets_string = fp.read()

all_tweets_dicts = json.loads(tweets_string)
all_tweets_dicts.append(tweet_dict)
serialized_tweets_list = json.dumps(all_tweets_dicts, indent=4, separators=(",",":"))

#dump to json file
with open("tweets.json", "w+") as fp:
	fp.write(serialized_tweets_list)