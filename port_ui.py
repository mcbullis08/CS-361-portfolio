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


# necessary library's
import time
import geocoder
import json
import search


# Paths and global variables
read_camp_path = 'campgrounds.txt'
write_coord_path = 'coordinates.txt'

write_zip_path = 'zipcode.txt'
write_day_path = 'days_out.txt'

read_weather = 'weather_data.txt'
read_activities = 'activities.txt'

bing_key = 'AtVAJAr_86Xhp3cOeTrjVCfW6T68GUdkCFvBAx4T2nIhiwYVW9p17UhKcGUff0TS'


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
    # Function to read in user data and return that info for storage to main

    print()
    print('First we will need to get the location where you would like to go camping.')
    location = input('Please enter that now. (City,State or Zip):')
    print(location)
    print()
    print('Great choice! Now how far from this location would you be willing to camp?')
    dist = input('Enter a range (max of 25 miles) from this location:')
    print(dist + ' miles')
    print()

    info = [location, dist]
    return info


def convert_location(location):
    # function to convert the supplied city, st with a suitable latitude and longitude
    # and zipcode for use by partner's microservice

    geo_location = geocoder.bing(location, key=bing_key, method='reverse')
    result = geo_location.json
    location_data = [result['lat'], result['lng'], result['postal']]
    return location_data


def write_to_files(all_data):
    # function to write necessary info to files for further processing

    coordinates = [all_data[0], all_data[1], all_data[3]]
    zip_code = all_data[2]

    with open(write_coord_path, 'w') as write:
        for x in coordinates:
            write.write(f"{x}\n")
        write.close()

    print("Here is the zipcode for the location you wish to stay: " + zip_code)


def distill_weather():
    # function to write selected weather data to file for printing later

    with open(read_weather, 'r') as r:
        raw_weather = json.loads(r.read())

    weather_list = [['Date       ', 'High', 'Low  ', 'Conditions   ']]

    for i in raw_weather['forecast']['forecastday']:
        weather_list.append([i['date'], i['day']['maxtemp_f'], i['day']['mintemp_f'], i['day']['condition']['text']])

    with open(read_weather, 'w') as write:
        for sub in weather_list:
            for x in sub:
                write.write(str(x) + ' ')
            write.write('\n')
        write.close()


def print_to_screen():
    # function to pretty print the campground list, weather, and nearby activities

    print('Here is your list of campgrounds:')
    with open(read_camp_path, 'r') as r:
        camp_contents = r.read()
        print(camp_contents)

    input("Press enter to continue...")
    print()

    print('Here is the weather report for your length of stay:')
    with open(read_weather, 'r') as r:
        weather_contents = r.read()
        print(weather_contents)

    input("Press enter to continue...")
    print()

    print('Here are some activities of interest in your area')
    with open(read_activities, 'r') as r:
        activities_contents = r.read()
        print(activities_contents)


def goodbye():
    # Function to thank the user, provide them with the link to make
    # a reservation and end the program

    print()
    print('Here is the website where you can go and book the campground of your choice -')
    print('https://www.recreation.gov/')
    print()
    print('Thank you for using Campground Finder 1.0! Get out there and have fun!')


def main():
    greeting()

    while True:

        get_data = get_user_data()
        user_location, user_dist = get_data[0], get_data[1]

        get_loc = convert_location(user_location)
        get_loc.append(user_dist)

        write_to_files(get_loc)

        search.main()

        time.sleep(15)

        distill_weather()

        print_to_screen()

        print("Press enter to run another search or you can type 'quit' to quit.")
        temp = input()

        if temp != 'quit':
            continue
        else:
            break

    goodbye()


if __name__ == "__main__":
    main()



