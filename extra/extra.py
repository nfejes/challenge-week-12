import sys, json, time, re
from pymongo import MongoClient
mongo = MongoClient('localhost',27017)

review = mongo['yelp']['review']

texts = review.find({'date': '2010-05-25'},{'text':1})#.limit(100000)

nonchar = re.compile('[^a-z\'\\s]')
space   = re.compile('\\s+')

tuples = {}
for text in texts:
	text = nonchar.sub('',text['text'].lower())
	text = space.sub(',',text)
	words = text.split(',')
	for k in range(len(words)-1):
		key = (words[k],words[k+1])
		if key in tuples:
			tuples[key] += 1
		else:
			tuples[key] = 1


for count,words in sorted([(tuples[k],k) for k in tuples.keys()], reverse=True)[:20]:
	print "(%s,%s): %d" % (str(words[0]),str(words[1]),count)




