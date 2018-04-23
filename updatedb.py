import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hug_project.settings')
import django
django.setup()

import urllib
import zipfile
import xml.etree.ElementTree as ET
import urllib2
import json
from hug.models import Tree

# state max number of files
MAX_TREESTOTAL = 200
MAX_TREEPERFILE = 10
TESTING = True

def populate():
    # initalize all counters
    counterfiles = 0
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
    zip, headers = urllib.urlretrieve('ftp://webftp.vancouver.ca/OpenData/xml/xml_street_trees.zip')
    with zipfile.ZipFile(zip, 'r') as zf:
        # get names of all xml files in zip
        xmlfiles = [name for name in zf.namelist()
                    if name.endswith('.xml')]
        # get rid of StreetTrees_CityWide.xml because this db is corrupt
        if xmlfiles.count('StreetTrees_CityWide.xml') > 0:
            xmlfiles.remove('StreetTrees_CityWide.xml')
        # iterate through the xml files in zip
        for filename in xmlfiles:
            print(filename)
            files = zf.open(filename)
            parsedfiles = ET.parse(files)
            print 'total added: ', counterfiles
            if counterfiles >= MAX_TREESTOTAL:
                break
            countertrees = 0
            # iterate through all trees in a xml file
            for alltrees in parsedfiles.findall('StreetTree'):
                if countertrees >= MAX_TREEPERFILE or counterfiles >= MAX_TREESTOTAL:
                    break
                try:
                    # check if tree is already in db
                    treeId = alltrees.attrib['TreeID']
                    Tree.objects.get(treeId=treeId)
                    print ('That has already been planted in the database, baby')
                except Tree.DoesNotExist:
                    # get tree info
                    neighbourhood = alltrees.find('NeighbourhoodName').text
                    commonName = alltrees.find('CommonName').text
                    diameter = float(alltrees.find('Diameter').text)
                    streetNumber = alltrees.find('CivicNumber').text
                    street = alltrees.find('StdStreet').text
                    # beginning of lat lon parsing
                    newStreet = street
                    if newStreet[:2] == "W ":
                       newStreet = "WEST+" + newStreet[2:]
                    if newStreet[:2] == "E ":
                       newStreet = "EAST+" + newStreet[2:]
                    if newStreet[:2] == "N ":
                       newStreet = "NORTH+" + newStreet[2:]
                    if newStreet[:2] == "S ":
                       newStreet = "SOUTH+" + newStreet[2:]
                    newStreet = newStreet.replace(" ", "")
                    addressOfTree = str(streetNumber) + "+" + newStreet + "+Vancouver,BC"
                    print (addressOfTree)
                    # check if tree address already exists
                    if addressOfTree not in seen:
                        seen.add(addressOfTree)
                        try:
                            urlCall = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBdKoYAuijJFuO2XGawW1sjLf1w6fEUFlg&address="
                            fullUrlCall = urlCall + addressOfTree
                            response = urllib2.urlopen(fullUrlCall)
                            jsongeocode = response.read()
                            b = json.loads(jsongeocode)
                        except urllib2.HTTPError:
                            print("That address is the black sheep of the family, it looks like " + addressOfTree)
                        try:
                            lat = b['results'][0]['geometry']['location']['lat']
                            lon = b['results'][0]['geometry']['location']['lng']
                            #end of addition. Imported urllib2 and json and changed lat/lon below from 0
                            counterfiles += 1
                            countertrees += 1
                            add_tree(treeId=treeId, neighbourhood=neighbourhood, commonName=commonName,
                                    diameter=diameter, streetNumber=streetNumber, street=street,
                                    lat=lat, lon=lon)
                            print 'finished add ', countertrees
                        except ValueError:
                            print ("You and the tree were never meant to be")
                        except IndexError:
                            print ("This tree made like a tree and leaved...")
                    else:
                        print("A tree is already there! What the hell are you playing at?")

def test_populate():
    # initalize all counters
    counterfiles = 0
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
    #test that address to be added is not in db already
    assert "123+POOPST+Vancouver,BC" not in seen
    #test if a tree with address already in db
    assert "2633+GRANVILLEST+Vancouver,BC" in seen
    # created fake zip file locally
    zip = 'TreeTest.zip'
    with zipfile.ZipFile(zip, 'r') as zf:
        # get names of all xml files in zip
        xmlfiles = [name for name in zf.namelist()
                    if name.endswith('.xml')]
        # make sure TestTrees are added
        assert len(xmlfiles) == 2
        assert "file1.xml" in xmlfiles
        assert "file2.xml" in xmlfiles
        # iterate through the xml files in zip
        for filename in xmlfiles:
            print(filename)
            files = zf.open(filename)
            parsedfiles = ET.parse(files)
            print 'total added: ', counterfiles
            if counterfiles >= MAX_TREESTOTAL:
                break
            countertrees = 0
            # iterate through all trees in a xml file
            for alltrees in parsedfiles.findall('StreetTree'):
                if countertrees >= MAX_TREEPERFILE or counterfiles >= MAX_TREESTOTAL:
                    break
                try:
                    # check if tree is already in db
                    treeId = alltrees.attrib['TreeID']
                    Tree.objects.get(treeId=treeId)
                    # check that the tree that already exists doesnt get added again
                    print treeId, ' has already been planted in the database, baby'
                except Tree.DoesNotExist:
                    # get tree info
                    neighbourhood = alltrees.find('NeighbourhoodName').text
                    commonName = alltrees.find('CommonName').text
                    diameter = float(alltrees.find('Diameter').text)
                    streetNumber = alltrees.find('CivicNumber').text
                    street = alltrees.find('StdStreet').text
                    # beginning of lat lon parsing
                    newStreet = street
                    if newStreet[:2] == "W ":
                       newStreet = "WEST+" + newStreet[2:]
                    if newStreet[:2] == "E ":
                       newStreet = "EAST+" + newStreet[2:]
                    if newStreet[:2] == "N ":
                       newStreet = "NORTH+" + newStreet[2:]
                    if newStreet[:2] == "S ":
                       newStreet = "SOUTH+" + newStreet[2:]
                    newStreet = newStreet.replace(" ", "")
                    addressOfTree = str(streetNumber) + "+" + newStreet + "+Vancouver,BC"
                    print (addressOfTree)
                    # check if tree address already exists
                    if addressOfTree not in seen:
                        seen.add(addressOfTree)
                        # DO NOT CALL GOOGLE API FOR TEST! RETURN DUMMY DATA
                        lat = 0
                        lon = 0
                        counterfiles += 1
                        countertrees += 1
                        # DO NOT SAVE DUMMY DATA INTO DB!
                        # add_tree(treeId=treeId, neighbourhood=neighbourhood, commonName=commonName,
                        #         diameter=diameter, streetNumber=streetNumber, street=street,
                        #         lat=lat, lon=lon)
                        print treeId, neighbourhood, commonName, diameter, streetNumber, lat, lon
                        print 'added ', countertrees
                    else:
                        print("A tree is already there! What the hell are you playing at?")
    assert counterfiles == 3
    print ('end test')

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
    if TESTING:
        print "Starting test update..."
        test_populate()
    else:
        print "Starting update script..."
        populate()
