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
import geocoder
import geopy
import math


write_path = 'C:/Users/Jeremy/PycharmProjects/CS361/portfolio/coordinates.txt'
read_path = 'C:/Users/Jeremy/PycharmProjects/CS361/portfolio/campgrounds.txt'


def greeting():
    # Function to greet user and describe the project

    print()
    print('Hello! Welcome to campground finder 1.0!')
    print('This program will ask you to supply a location where you would like to go camping,')
    print('and a search radius. It will then return to you a list of campgrounds that are within')
    print('that radius from the location you supplied.')
    print('As a bonus, it will also give you the expected weather for the location, as well as,')
    print('some fun activities that you may be interested in that are near by.')


def get_user_data():

    print()
    print('First we will need to get the location where you would like to go camping.')
    location = input('Please enter that now. (City,State or Zip):')
    print(location)
    print()
    print('Great choice! Now how far from this location would you be willing to camp?')
    dist = input('Enter a range (max of 25 miles) from this location:')
    print(dist + ' miles')

    return location, dist


def convert_location(location):
    # function to convert the supplied city, st or zip with a suitable latitude and longitude
    bing_key = 'AtVAJAr_86Xhp3cOeTrjVCfW6T68GUdkCFvBAx4T2nIhiwYVW9p17UhKcGUff0TS'

    geo_location = geocoder.bing(location, key=bing_key)
    result = geo_location.json
    return result['lat'], result['lng']
    # write result to file here


def convert_dist(dist):
    # function to convert distance to a latitude and longitude adjustment
    # one degree latitude = 69 mi, one minute = 1.15 mi, one second = 101 ft
    # one degree longitude = 54.6 mi, one minute equals 0.91 mi, one second = 80 ft

    try:
        dist = int(dist)
    except ValueError:
        print("range is not a numerical value")

    lat_dist = dist/69
    lng_dist = dist/54.6

    return lat_dist, lng_dist


def boundary_box(lat_loc, lng_loc, lat_dist, lng_dist):
    # create a boundary box of latitude and longitude as our search area
    lat_max = lat_loc + lat_dist
    lat_min = lat_loc - lat_dist

    lng_max = lng_loc + lng_dist
    lng_min = lng_loc - lng_dist

    bound_box = [lat_max, lat_min, lng_max, lng_min]

    return bound_box


def goodbye():
    # Function to thank the user and end the program

    print()
    print('Thank you for using Campground Finder 1.0! Get out there and have fun!')


def main():

    greeting()

    get_data = get_user_data()
    user_location, user_dist = get_data[0], get_data[1]

    get_loc = convert_location(user_location)

    temp2 = convert_dist(user_dist)
    new_dist = temp2[0], temp2[1]

    # final = boundary_box(get_loc[0], get_loc[1], new_dist[0], new_dist[1])
    final = []
    for x in get_loc:
        final.append(x)
    final.append(user_dist)
    print(final)
    # write boundary box to file for further processing

    with open(write_path, 'w') as write:
        for x in final:
            write.write(f"{x}\n")
        write.close()

    time.sleep(3)

    with open(read_path, 'r') as r:
        lines = r.readlines()
        for line in lines:
            print(line)
        r.close

    goodbye()


if __name__ == "__main__":
    main()

