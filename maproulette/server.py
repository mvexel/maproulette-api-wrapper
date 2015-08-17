#!/usr/bin/env python

"""
A MapRoulette server.
"""

import re

import requests


class MapRouletteServer(object):
    """
    Typical usage::

        server = MapRouletteServer(
            url='http://maproulette.org/api',
            user=foo,
            password=bar)

    :param url: The URL for the MapRoulette API server you want to use. Example: `http://dev.maproulette.org/api`
    :type url: String
    :param user: Your username for this MapRoulette server's API
    :param password: Your password for this MapRoulette server's API
    :rtype: A :py:class:`MapRouletteServer`
    """

    ENDPOINTS = {
        'ping': '/ping',
        'challenges': '/challenges',
        'challenge': '/challenge/{slug}',
        'task': '/challenge/{slug}/task/{identifier}',
        'task_admin': '/admin/challenge/{slug}/task/{identifier}',
        'challenge_admin': '/admin/challenge/{slug}',
        'tasks_admin': '/admin/challenge/{slug}/tasks'
    }

    base_url = ''
    user = ''
    password = ''

    def __init__(self, user, password, url):
        self.base_url = url
        self.user = user
        self.password = password
        if not self.alive:
            raise Exception('server is not alive')

    def __build_url(self, endpoint, querystring=None, replacements=None):
        if endpoint not in self.ENDPOINTS:
            raise Exception('{} not in endpoints'.format(endpoint))
        url = self.base_url
        if replacements:
            url += self.ENDPOINTS[endpoint].format(**replacements)
        else:
            url += self.ENDPOINTS[endpoint]
        if querystring:
            url += '?{}'.format(querystring)
        return url

    @staticmethod
    def __is_admin_url(url):
        return re.search('/admin/', url) is not None

    def __auth_params_for(self, url):
        if self.__is_admin_url(url):
            return self.user, self.password
        return None

    @property
    def alive(self):
        url = self.__build_url('ping')
        try:
            response = requests.get(url)
        except Exception:
            return False
        if response.status_code != 200:
            return False
        return True

    def challenges(self):
        expect_status = 200
        url = self.__build_url('challenges')
        response = requests.get(url)
        if response.status_code != expect_status:
            raise Exception('server did not return as expected from {}. (Expected: {}, received: {})'.format(
                url,
                expect_status,
                response.status_code))
        return response.json()

    def get(self, endpoint, querystring=None, replacements=None):
        expect_status = 200
        url = self.__build_url(
            endpoint,
            querystring=querystring,
            replacements=replacements)
        response = requests.get(url, auth=self.__auth_params_for(url))
        if response.status_code != expect_status:
            raise Exception('server did not return as expected from {}. (Expected: {}, received: {})'.format(
                url,
                expect_status,
                response.status_code))
        return response.json()

    def post(self, endpoint, payload, replacements=None):
        expect_status = 201
        url = self.__build_url(
            endpoint,
            replacements=replacements)
        response = requests.post(url, json=payload, auth=self.__auth_params_for(url))
        if response.status_code != expect_status:
            raise Exception('server did not return as expected from {}. (Expected: {}, received: {})'.format(
                url,
                expect_status,
                response.status_code))
        return response.json()

    def put(self, endpoint, payload, replacements=None):
        expect_status = 200
        url = self.__build_url(
            endpoint,
            replacements=replacements)
        response = requests.put(url, json=payload, auth=self.__auth_params_for(url))
        if response.status_code != expect_status:
            raise Exception('server did not return as expected from {}. (Expected: {}, received: {})'.format(
                url,
                expect_status,
                response.status_code))
        return response.json()

    def delete(self, endpoint, replacements=None):
        expect_status = 204
        url = self.__build_url(
            endpoint,
            replacements=replacements)
        response = requests.delete(url, auth=self.__auth_params_for(url))
        if response.status_code != expect_status:
            raise Exception('server did not return as expected from {}. (Expected: {}, received: {})'.format(
                url,
                expect_status,
                response.status_code))
        return True
