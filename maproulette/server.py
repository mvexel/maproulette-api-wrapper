#!/usr/bin/env python

import requests

class MapRouletteServer(object):
    """A MapRoulette server"""

    MAPROULETTE_PRODUCTION_URL = 'http://maproulette.org/api'
    ENDPOINTS = {
        'ping'      :       '/ping',
        'challenges':       '/challenges'
    }

    base_url = ''

    def __init__(self, url=MAPROULETTE_PRODUCTION_URL):
        self.base_url = url
        print 'inited with base url {}'.format(self.base_url)

    def alive(self):
        response = requests.get(self.base_url + self.ENDPOINTS['ping'])
        if not response.ok:
            return False
        return True

    def challenges(self):
        response = requests.get(self.base_url + self.ENDPOINTS['challenges'])
        if not response.ok:
            return False
        return response.json()
