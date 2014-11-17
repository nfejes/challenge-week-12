
import sys, json, time
from pymongo import MongoClient
mongo = MongoClient('localhost',27017)

filename = sys.argv[1]

# get number of objects in file
count = sum(1 for line in open(filename))-1

f = open(filename)

headers = f.readline().lower().replace('-','_').replace('hly_','').split(',')

collection = mongo['weather']['precipitation']

timer = [0,0,time.time()]
while True:
	line = f.readline().strip()
	if line == '': break

	csv = line.split(',')
	#STATION,STATION_NAME,ELEVATION,LATITUDE,LONGITUDE,DATE,HPCP,Measurement Flag,Quality Flag 
	jsondata = {
		'station' : csv[0],
		'station_name' : csv[1],
		'location' : {
			'type':   "Point", 
			'elevation' : csv[2],
			'coordinates': [float(csv[4]),float(csv[3])]
		},
		'date' : csv[5]
	}
	if csv[6] and not csv[6] == '99999': jsondata['hpcp'] = float(csv[6])
	if csv[7]: jsondata['measurement_flag'] = csv[7]
	if csv[8]: jsondata['quality_flag'] = csv[8]

	collection.insert(jsondata)
	timer[0] += 1

	t = time.time()
	if t - timer[2] > 1:
		n = len(str(count))
		tot = timer[0] + timer[1]
		print 'imported %*d/%*d (%d rows/s, %4.1f%%)' % (n,tot,n,count,timer[0],100*tot/float(count))
		timer = [0,tot,t]

n = len(str(count))
tot = timer[0] + timer[1]
print 'imported %*d/%*d (%d rows/s, %4.1f%%)' % (n,tot,n,count,timer[0],100*tot/float(count))


