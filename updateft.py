import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hug_project.settings')
import django
django.setup()

import csv
import urllib2
from hug.models import FoodTree

TESTING = True

def populate():
    # get url of the csv file
    url = 'ftp://webftp.vancouver.ca/OpenData/csv/CommunityGardensandFoodTrees.csv'
    response = urllib2.urlopen(url)
    file = csv.DictReader(response)
    count = 0
    for row in file:
        if row["NumberOfFoodTrees"] is not '':
            name = str(row["Name"])
            address = str(row["MergedAddress"])
            address = ''.join([i if ord(i) < 128 else ' ' for i in address])
            lat = row["Latitude"]
            lon = row["Longitude"]
            numOfFT = row["NumberOfFoodTrees"]
            if numOfFT is 'Y':
                numOfFT = None
            typesOfFT = str(row["FoodTreeVarieties"])
            typesOfFT = ''.join([i if ord(i) < 128 else ' ' for i in typesOfFT])
            print "adding", name
            count += 1
            print count
            add_ft(name=name, address=address, lat=lat, lon=lon, numOfFT=numOfFT,
                   typesOfFT=typesOfFT, neighbourhood="")

def test_populate():
    #load in dummy data file
    file = csv.DictReader(open("FTTest.csv"))
    count = 0
    for row in file:
        if row["NumberOfFoodTrees"] is not '':
            name = str(row["Name"])
            address = str(row["MergedAddress"])
            address = ''.join([i if ord(i) < 128 else ' ' for i in address])
            lat = row["Latitude"]
            lon = row["Longitude"]
            numOfFT = row["NumberOfFoodTrees"]
            if numOfFT is 'Y':
                numOfFT = None
            typesOfFT = str(row["FoodTreeVarieties"])
            typesOfFT = ''.join([i if ord(i) < 128 else ' ' for i in typesOfFT])
            print "adding", name
            count += 1
            print count
            # DO NOT LOAD IN DUMMY DATA!
            # add_ft(name=name, address=address, lat=lat, lon=lon, numOfFT=numOfFT,
            #        typesOfFT=typesOfFT, neighbourhood="")
            print name, address, lat, lon, numOfFT, typesOfFT
        else:
            print str(row["Name"]), "has no foodtrees!"
    assert count == 2
    print "finish test"

def add_ft(name, address, lat, lon, numOfFT, typesOfFT,neighbourhood):
    ft = FoodTree.objects.get_or_create(name=name)[0]
    ft.address = address
    ft.lat = lat
    ft.lon = lon
    ft.numOfFT = numOfFT
    ft.typesOfFT = typesOfFT
    ft.neighbourhood = neighbourhood
    ft.save()
    return ft

# Start execution here!
if __name__ == '__main__':
    if TESTING:
        print "Starting test FoodTrees update..."
        test_populate()
    else:
        print "Starting FoodTrees update script..."
        populate()
