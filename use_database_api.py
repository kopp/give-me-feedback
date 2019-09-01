#!/usr/bin/env python


# Documentation:
# https://firebase.google.com/docs/reference/rest/database

# Database is at
# https://give-me-feedback.firebaseio.com
# To access top-level element 'foo', access
# base_url + foo.json
# To access any other nested element, use
# base_url + path_to_element + '.json'

# To read data, use GET
# To (overwrite) data, use PUT
# To append data, use POST -- this will create a new element with random name with the given children

# For authentication, see
# https://firebase.google.com/docs/database/rest/auth
# for how to create/use an access token.


import requests
import json
import sys
import pprint


BASE_URL = 'https://give-me-feedback.firebaseio.com/'


class Database:
    def __init__(self, base_url):
        self.base_url = base_url

    def append(self, location, content):
        '''Append content (python map) at location in the database.
        Raise in case of error.
        '''
        r = requests.post(self.base_url + location + '.json', json.dumps(content))
        if not r.ok:
            raise ValueError('Error {} when appending {} at {}'.format(
                r.text, content, location))

    def get(self, location):
        '''Return data from given location as python object.'''
        r = requests.get(self.base_url + location + '.json')
        if r.ok:
            return r.json()
        else:
            raise ValueError('Error {} when trying to access {}'.format(
                r.text, location))


def _manual_test():
    database = Database(BASE_URL)
    database.append('/test', {'foo': 'bar'})
    test = database.get('/test')
    print(test)


def interactive(argv):
    import argparse

    parser = argparse.ArgumentParser(description='Use the Database API to read/write')
    parser.add_argument('--get', type=str, metavar='/location/in/database',
                        help='get the given location in the database')

    args = parser.parse_args(argv)

    database = Database(BASE_URL)
    printer = pprint.PrettyPrinter(indent=2)

    if args.get:
        data = database.get(args.get)
        printer.pprint(data)


if __name__ == '__main__':
    interactive(sys.argv[1:])
