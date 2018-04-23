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

def startSteal():

    fullJSONString = "{" + "\n" + """"trees": [ """

    all_Trees = Tree.objects.all()
    for x in all_Trees:
        me = Object()
        me.treeId = x.treeId
        me.neighbourhood = x.neighbourhood
        me.commonName = x.commonName
        me.diameter = x.diameter
        me.streetNumber = x.streetNumber
        me.street = x.street
        me.lat = x.lat
        me.lon = x.lon
        print ('Found a full tree')
        fullJSONString = fullJSONString + "\n" + me.to_JSON() + ","

    fullJSONString = fullJSONString + "]}"

    text_file = open("StolenJson.txt", "w")
    text_file.write(fullJSONString)
    text_file.close()

# Start execution here!
if __name__ == '__main__':
    print "Starting steal script..."
    startSteal()