import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hug_project.settings')
import django
django.setup()

import csv
import urllib
import zipfile
import urllib2
import json
from hug.models import Park

TESTING = False

def populate():
    # get url of the csv file
    zip, headers = urllib.urlretrieve('ftp://webftp.vancouver.ca/opendata/csv/csv_parks_facilities.zip')
    with zipfile.ZipFile(zip, 'r') as zf:
        filename = 'parks.csv'
        response = zf.open(filename)
        file = csv.DictReader(response)
        count = 0
        for row in file:
            parkId = int(row["ParkID"])
            name = str(row["Name"])
            address = str(row["StreetNumber"]) + " " + str(row["StreetName"])
            GoogleMapDest = row["GoogleMapDest"]
            lat = GoogleMapDest.split(',', 1)[0]
            lon = GoogleMapDest.split(',', 1)[-1]
            neighbourhood = str(row["NeighbourhoodName"])
            count += 1
            print count
            add_park(parkId=parkId, name=name, address=address, lat=lat, lon=lon, neighbourhood=neighbourhood)

def test_populate():
    #load in dummy data zip
    zip = 'TestParks.zip'
    with zipfile.ZipFile(zip, 'r') as zf:
        filename = 'parks.csv'
        response = zf.open(filename)
        file = csv.DictReader(response)
        count = 0
        for row in file:
            parkId = int(row["ParkID"])
            name = str(row["Name"])
            address = str(row["StreetNumber"]) + " " + str(row["StreetName"])
            GoogleMapDest = row["GoogleMapDest"]
            lat = GoogleMapDest.split(',', 1)[0]
            lon = GoogleMapDest.split(',', 1)[-1]
            neighbourhood = str(row["NeighbourhoodName"])
            count += 1
            print count
            # DO NOT ADD DUMMY DATA INTO DB!
            # add_park(parkId=parkId, name=name, address=address, lat=lat, lon=lon, neighbourhood=neighbourhood)
            print parkId, name, address, lat, lon, neighbourhood
    assert count == 4

def add_park(parkId, name, address, lat, lon, neighbourhood):
    park = Park.objects.get_or_create(parkId=parkId)[0]
    park.name = name
    park.address = address
    park.lat = lat
    park.lon = lon
    park.neighbourhood = neighbourhood
    park.save()
    return park

# Start execution here!
if __name__ == '__main__':
    if TESTING:
        print "Starting test Park update..."
        test_populate()
    else:
        print "Starting Park update script..."
        populate()
