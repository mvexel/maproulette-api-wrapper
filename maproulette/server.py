#!/usr/bin/env python

import requests

class MapRouletteServer(object):
    """A MapRoulette server"""

    MAPROULETTE_PRODUCTION_URL = 'http://maproulette.org/api'
    ENDPOINTS = {
        'ping'      : '/ping',
        'challenges': '/challenges',
        'tasks'     : '/admin/challenge/{}/tasks'
    }

    base_url = ''
    active_challenge = None

    def __init__(self, url=MAPROULETTE_PRODUCTION_URL, challenge=None):
        self.base_url = url
        self.active_challenge = challenge

    def alive(self):
        response = requests.get(self.base_url + self.ENDPOINTS['ping'])
        if not response.ok:
            return False
        return True

    def challenges(self):
        response = requests.get(self.base_url + self.ENDPOINTS['challenges'])
        if not response.ok:
            return None
        return response.json()

    def tasks(self):
        if not self.active_challenge:
            return None
        print self.base_url + self.ENDPOINTS['tasks'].format(self.active_challenge)
        response = requests.get(
            self.base_url + self.ENDPOINTS['tasks'].format(self.active_challenge))
        return response.json()