import sys, json, time
from pymongo import MongoClient
mongo = MongoClient('198.199.113.194',27017)

reddit = mongo['bigdata']['reddit']

# Load query from file
try:
	commenters = json.load(open('top50comments.json'))
	subreddits = commenters.keys()

# Read from mongo
except IOError:
	print 'Aggregating top 50...'
	top50 = reddit.aggregate([
		{'$group': {'_id':'$subreddit', 'comments': {'$sum': 1}}},
		{'$sort':  {'comments': -1}},
		{'$limit': 50}
	])['result']
	subreddits = [str(x[u'_id']) for x in top50]
	
	print 'Aggregating commenters...'
	commenters = {}
	for sr in subreddits:
		print 'for ' + sr + '...'
		c = reddit.find({'subreddit': sr}).distinct('author')
		commenters[sr] = c
		print 'got %d commenters' % len(c)

	open('top50icomments.json','w').write(json.dumps(commenters))
	

# Convert lists to sets
commenters = { k : set(commenters[k]) for k in subreddits }

# Compute similiarity (#(common commenters) / #(unique commenters))
pairs = []
for i,k1 in enumerate(subreddits):
	for k2 in subreddits[i+1:]:
		common = len(commenters[k1] & commenters[k2]) / float(len(commenters[k1] | commenters[k2]))
		pairs.append((common, k1, k2))

# Print top 30
for (c,k1,k2) in sorted(pairs, reverse=True)[:30]:
	print "(%s,%s): %.2f%%" %(k1,k2,100*c)

