import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hug_project.settings')
import django
django.setup()

import urllib
import zipfile
import xml.etree.ElementTree as ET
import urllib2
import json
import collections
from hug.models import Tree

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def startSplit():

    #Read a JSON file

    with open('C:\Users\Zim\Documents\GitHub\TimeTravellingTrout\hug_project\JSON.txt') as data_file:
        data = json.load(data_file)

    howManyTrees = len(data['trees'])
    print (str(howManyTrees))

    seen = set()

    #Check for unseen neighbourhood

    try:
        for x in range(0, howManyTrees):
            theTree = data['trees'][x]
            neighbourhood = theTree['neighbourhood']
            if neighbourhood not in seen:
                seen.add(neighbourhood)
    except ValueError:
        print('Value Error')
    except IndexError:
        print('Index Error')

    #Search through full file for trees with that neighbourhood

    try:
        for item in seen:
            fullJSONString = "{" + "\n" + """"trees": [ """
            loopNum = 0

            while loopNum != howManyTrees:
                thisTree = data['trees'][loopNum]
                #print(str(thisTree['treeId']))
                checkNeighbourhood = thisTree['neighbourhood']
                loopNum = loopNum + 1
                if checkNeighbourhood == item:
                    currentStringObj = "\n" + "{\n\t" + \
                    '"commonName": "' + thisTree['commonName'] + '",\n\t' + \
                    '"diameter": ' + str(thisTree['diameter']) + ",\n\t" + \
                    '"lat": ' + str(thisTree['lat']) + ",\n\t" + \
                    '"lon": ' + str(thisTree['lon']) + ",\n\t" + \
                    '"neighbourhood": "' + thisTree['neighbourhood'] + '",\n\t' + \
                    '"street": "' + thisTree['street'] + '",\n\t' + \
                    '"streetNumber": ' + str(thisTree['streetNumber']) + ",\n\t" + \
                    '"treeId": ' + str(thisTree['treeId']) + "\n},"
                    fullJSONString = fullJSONString + currentStringObj
                    print(currentStringObj)
            text_file = open(item + ".txt", "w")
            fullJSONString = fullJSONString + "}]}"
            text_file.write(str(fullJSONString))
            text_file.close()
    except ValueError:
        print('Value Error @' + str(thisTree['treeId']) + "in iter " + str(loopNum))
    except IndexError:
        print('Index Error')

# Start execution here!
if __name__ == '__main__':
    print "Starting split script..."
    startSplit()