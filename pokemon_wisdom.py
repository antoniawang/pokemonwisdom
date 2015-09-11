import nltk
import random
from quotes import raw_quotes
from pokemon_names import names

#Choose a random Pokemon index number
pokemon_index = random.randint(0, len(names))
#print pokemon_index
pokemon_selected = names[pokemon_index]
#print pokemon_selected


#Turn raw quotes into a list of tuples (quote, author)
quotes = []
#print len(raw_quotes)

for i in range(0, len(raw_quotes), 2):
	quotes.append((raw_quotes[i],raw_quotes[i+1]))


#Choose a random quote
quote_selected = random.choice(quotes)
# print quote_selected

#quote = random.choice(quotes)
text = nltk.word_tokenize(quote_selected[0])



#Find a random noun in the quote
noun_tags = ["NN","NNS","NNP","NNPS","PRP"]
quote_split = nltk.pos_tag(text)
# print quote_split
nouns = [word for word, part in quote_split if part in noun_tags]
# print nouns
noun_to_replace = random.choice(nouns) #need to take out repeats
# print noun_to_replace

quote_selected = (quote_selected[0].replace(noun_to_replace,pokemon_selected), quote_selected[1])


tweet = quote_selected[0] + " " + quote_selected[1] + " #pokemon #wisdom"

print tweet

#tweet = "\n".join(quote)

if len(tweet) > 280:
	print tweet
	print len(tweet)




