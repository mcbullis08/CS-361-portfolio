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

import requests


read_path = 'coordinates.txt'
write_path = 'campgrounds.txt'
rec_area_path = 'rec_area.txt'
activities_path = 'activities.txt'

rec_gov_api = '30341f7c-0b1b-4460-ade0-40346cb25308'

facility_url = 'https://ridb.recreation.gov/api/v1/facilities'
activities_url = 'https://ridb.recreation.gov/api/v1/recareas/'


def get_campgrounds():
    data = []

    with open(read_path, 'r') as r:
        lines = r.readlines()
        r.close()

    for line in lines:
        data.append(line.strip().split('\n'))

    headers = {
        'accept': 'application / json',
        'apikey': rec_gov_api
        }

    params = {'latitude': data[0], 'longitude': data[1], 'radius': data[2]}

    r = requests.get(facility_url, headers=headers, params=params)

    results = r.json()

    return results


def get_activities():
    activities = []

    headers = {
        'accept': 'application / json',
        'apikey': rec_gov_api
    }

    with open(rec_area_path, 'r') as r:
        line = r.readline()
        while line:
            url = activities_url + line.strip() + '/activities'
            results = requests.get(url, headers=headers).json()
            for i in results['RECDATA']:
                activities.append(i['ActivityName'])
            line = r.readline()
        r.close()

    with open(activities_path, 'w') as write:
        for x in list(set(activities)):
            write.write(f"{x}\n")
        write.close()


def write_to_file(result_data):

    campgrounds = []
    campground_list = []
    rec_area = []

    for i in result_data['RECDATA']:
        if i['FacilityTypeDescription'] == 'Campground':
            campgrounds.append(i)
            rec_area.append(i['ParentRecAreaID'])

    for idx, campsite in enumerate(campgrounds):
        name = campgrounds[idx]['FacilityName']
        campground_list.append(name)

    with open(write_path, 'w') as write:
        for x in campground_list:
            write.write(f"{x}\n")
        write.close()

    with open(rec_area_path, 'w') as write:
        for x in list(set(rec_area)):
            write.write(f"{x}\n")
        write.close()


def main():

    campgrounds = get_campgrounds()

    write_to_file(campgrounds)

    get_activities()


if __name__ == "__main__":
    main()

