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
        self.token = None

    def set_token(self, token):
        self.token = token

    def __get_default_params(self):
        params = {}
        if self.token:
            params['auth'] = self.token
        return params

    def __get_url(self, location):
        url = self.base_url + location + '.json'
        return url

    @staticmethod
    def __jsonify_content(content):
        '''Make sure that content is valid json.'''
        try:
            _ = json.loads(content)
            return content  # valid json
        except ValueError:
            return json.dumps(content)

    def append(self, location, content):
        '''Append content (python map) at location in the database.
        This will create a nested element with random name.
        Raise in case of error.
        '''
        return self.__upload_data(location, content, 'appen')

    def update(self, location, content):
        '''Add/update content at location; this will add the given key/values below an existing key.'''
        return self.__upload_data(location, content, 'update')

    def __upload_data(self, location, content, operation):
        '''Common implementation for POST and PATCH calls.'''
        KNOWN_OPERATIONS = {
            'append': ('POST', 'appending'),
            'update': ('PATCH', 'updating'),
        }
        try:
            method, description = KNOWN_OPERATIONS[operation]
        except KeyError:
            raise KeyError('Invalid method {} used in __upload_data'.format(operation))
        r = requests.request(method,
                             url=self.__get_url(location),
                             data=self.__jsonify_content(content),
                             params=self.__get_default_params()
                             )
        if not r.ok:
            raise ValueError('Error {} when {} {} at {}'.format(
                r.text, description, content, location))
        else:
            return True



    def get(self, location):
        '''Return data from given location as python object.'''
        r = requests.get(self.__get_url(location), self.__get_default_params())
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
    parser.add_argument('--append', nargs=2, metavar=('/location/in/database', '<CONTENT>'),
                        help='append CONTENT below the given location with a random key')
    parser.add_argument('--update', nargs=2, metavar=('/location/in/database', '<CONTENT>'),
                        help='add/update CONTENT at the given location')
    parser.add_argument('--token', type=str, metavar='<TOKEN>',
                        help='Access token for privileged database access.')

    args = parser.parse_args(argv)

    database = Database(BASE_URL)
    printer = pprint.PrettyPrinter(indent=2)

    if args.token:
        database.set_token(args.token)

    if args.get:
        data = database.get(args.get)
        printer.pprint(data)

    if args.append:
        location, content = args.append
        worked = database.append(location, content)
        if worked:
            print('done')

    if args.update:
        location, content = args.update
        worked = database.update(location, content)
        if worked:
            print('done')


if __name__ == '__main__':
    interactive(sys.argv[1:])
