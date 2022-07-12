# author: Jeremy Bullis (931241057)
# date: 7/5/22
# class: CS 361
# description: This will be the UI portion of my portfolio project. Right now we are going to building a
#              rudimentary campground finder. Essentially the user will be prompted with some information
#              and asked to input some information.
#
#              The program will then run the location and radius and pull some campground API information
#              in another service. The data will be processed and then displayed back to the user in the
#              form a list of campgrounds within the given radius of a specified location.
#
#              My partner will be providing another service which will return weather and activity
#              information that is located near the supplied destination to aid the user in selecting a
#              campground.

import time
import requests


read_path = 'C:/Users/Jeremy/PycharmProjects/CS361/portfolio/coordinates.txt'
write_path = 'C:/Users/Jeremy/PycharmProjects/CS361/portfolio/campgrounds.txt'

rec_gov_api = '30341f7c-0b1b-4460-ade0-40346cb25308'

url = 'https://ridb.recreation.gov/api/v1/facilities'

data = []


while True:

    time.sleep(3)

    with open(read_path, 'r') as r:
        lines = r.readlines()
        r.close()

    for line in lines:
        data.append(line.strip().split('\n'))

    headers = {
        'accept': 'application / json',
        'apikey': '30341f7c-0b1b-4460-ade0-40346cb25308'
    }

    params = {'latitude': data[0], 'longitude': data[1], 'radius': data[2], 'FacilityTypeDescription': 'Campground'}

    r = requests.get(url, headers=headers, params=params)

    results = [x for x in r.json()['RECDATA'] if x['FacilityTypeDescription'] == 'Campground']

    campgrounds = []

    for idx, campsite in enumerate(results):
        name = results[idx]['FacilityName']
        campgrounds.append(name)

    with open(write_path, 'w') as write:
        for x in campgrounds:
            write.write(f"{x}\n")
        write.close()

