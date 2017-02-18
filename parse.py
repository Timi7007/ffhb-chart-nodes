#! /usr/bin/env python
import json
import dateutil.parser
import urllib2
HAGEN_LON_MIN = 8.631391525
HAGEN_LON_MAX = 8.664050102
HAGEN_LAT_MIN = 53.347861457
HAGEN_LAT_MAX = 53.363921254
f = urllib2.urlopen(
    "https://downloads.bremen.freifunk.net/data/nodes.json")
js = open("data.js", 'w')
data = json.loads(f.read())
data = data['nodes']
HAGEN = []
BRE = []
totalclients = 0
clientsHAGEN = 0
for node in data:
    if 'location' in data[node]['nodeinfo'].keys():
        firstseen = data[node]['firstseen']
        latitude = data[node]['nodeinfo']['location']['latitude']
        longitude = data[node]['nodeinfo']['location']['longitude']
        hostname = data[node]['nodeinfo']['hostname']
        clients = data[node]['statistics']['clients']
        if((latitude > HAGEN_LAT_MIN) and (latitude < HAGEN_LAT_MAX) and
                (longitude > HAGEN_LON_MIN) and
                (longitude < HAGEN_LON_MAX)):
            HAGEN.append(firstseen)
            clientsHAGEN += data[node]['statistics']['clients']
    BRE.append(data[node]['firstseen'])
    totalclients += data[node]['statistics']['clients']

HAGEN = sorted(HAGEN)
BRE = sorted(BRE)


def toJS(data, label, file):
    file.write(label + " = [\n")
    current = 0
    for firstseen in data:
        firstseen = dateutil.parser.parse(firstseen)
        current = current + 1
        year = firstseen.year
        month = firstseen.month - 1
        day = firstseen.day
        file.write("{x: new Date(" + str(year) + "," + str(month) +
                    "," + str(day) + "), y: " + str(current) + "},\n")
    file.write("]\n")

toJS(HAGEN, "HAGEN", js)
toJS(BRE, "BRE", js)


js.write("clients = " + str(totalclients) + "\n")
js.write("clientsHAGEN = " + str(clientsHAGEN) + "\n")
