
import sys, json, time
from pymongo import MongoClient
mongo = MongoClient('localhost',27017)

f = open(sys.argv[1])

headers = f.readline().lower().replace('-','_').replace('hly_','').split(',')
#print headers

collection = mongo['weather']['normals']

line = f.readline()
timer = [0,time.time()]
while True:
	line = line.strip()

	csv = line.split(',')
	jsondata = {
		'station' : csv[0],
		'station_name' : csv[1],
		'elevation' : csv[2],
		'location' : {
			 'type':   "Point", 
			 'coordinates': [float(csv[4]),float(csv[3])]
		},
		'date' : csv[5]
	}

	comp = {}
	data = {}
	for i,v in enumerate(csv[6:]):
		if i%2 == 0:
			hi = 6 + i
			data[headers[hi]] = float(v)
		else:
			hi = 6 + i - 1
			comp[headers[hi]] = v

	jsondata['completeness'] = comp
	jsondata['data'] = data

	collection.insert(jsondata)
	timer[0] += 1

	t = time.time()
	if t - timer[1] > 1:
		print 'imported %d' % timer[0]
		timer = [0,t]

	line = f.readline()
	if line == '': break



