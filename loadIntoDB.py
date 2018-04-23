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

def loadIntoDB():

    seen = set()
    all_Trees = Tree.objects.all()

    for x in all_Trees:
        currStreetN = x.streetNumber
        currStreet = x.street
        if currStreet[:2] == "W ":
           currStreet = "WEST+" + currStreet[2:]
        if currStreet[:2] == "E ":
           currStreet = "EAST+" + currStreet[2:]
        if currStreet[:2] == "N ":
           currStreet = "NORTH+" + currStreet[2:]
        if currStreet[:2] == "S ":
           currStreet = "SOUTH+" + currStreet[2:]
        newCurrStreet = currStreet.replace(" ", "")
        seenAddress = str(currStreetN) + "+" + newCurrStreet + "+Vancouver,BC"
        print(seenAddress + "added to seen list")
        seen.add(seenAddress)
    # get url of the zipfile

    with open('C:\Users\Zim\Documents\GitHub\TimeTravellingTrout\hug_project\JSON.txt') as data_file:
        data = json.load(data_file)

    howManyTrees = len(data['trees']) - 1
    print(str(howManyTrees))

    try:
        for x in range(0, howManyTrees):
             try:
                # check if tree is already in db
                theTree = data['trees'][x]
                Tree.objects.get(treeId=theTree['treeId'])
                print ('That has already been planted in the database, baby')
             except Tree.DoesNotExist:
                treeId = theTree['treeId']
                neighbourhood= theTree['neighbourhood']
                commonName = theTree['commonName']
                diameter = theTree['diameter']
                streetNumber = theTree['streetNumber']
                street = theTree['street']
                lat = theTree['lat']
                lon = theTree['lon']
                add_tree(treeId=treeId, neighbourhood=neighbourhood, commonName=commonName,
                                    diameter=diameter, streetNumber=streetNumber, street=street,
                                    lat=lat, lon=lon)
    except ValueError:
        print ("You and the tree were never meant to be")
    except IndexError:
        print ("This tree made like a tree and leaved...")

def add_tree(treeId, neighbourhood, commonName, diameter, streetNumber, street, lat, lon):
    tree = Tree.objects.get_or_create(treeId=treeId)[0]
    tree.neighbourhood = neighbourhood
    tree.commonName = commonName
    tree.diameter = diameter
    tree.streetNumber = streetNumber
    tree.street = street
    tree.lat = lat
    tree.lon = lon
    tree.save()
    return tree

# Start execution here!
if __name__ == '__main__':
    print ("Starting update script...")
    loadIntoDB()
