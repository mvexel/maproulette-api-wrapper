#!/usr/bin/env python

import requests
import json

class MapRouletteServer(object):
	"""A MapRoulette server"""

	SERVERS = {
		'local'	 : 'http://localhost:5000/api',
		'dev'	   : 'http://dev.maproulette.org/api',
		'production': 'http://maproulette.org/api'}

	ENDPOINTS = {
		'ping'		   : '/ping',
		'challenges'	 : '/challenges',
		'challenge'	  : '/challenge/{slug}',
		'task'		   : '/challenge/{slug}/task/{identifier}',
		'task_admin'	 : '/admin/challenge/{slug}/task/{identifier}',
		'challenge_admin': '/admin/challenge/{slug}',
		'tasks_admin'	: '/admin/challenge/{slug}/tasks'
	}

	base_url = ''

	def __init__(self, instance='local'):
		self.base_url = self.SERVERS[instance]
		if not self.alive():
			raise MapRouletteServerException('server is not alive')

	def __build_url(self, endpoint, querystring=None, replacements=None):
		if endpoint not in self.ENDPOINTS:
			raise MapRouletteServerException('{} not in endpoints'.format(endpoint))
		url = self.base_url
		if replacements:
			url += self.ENDPOINTS[endpoint].format(**replacements)
		else:
			url += self.ENDPOINTS[endpoint]
		if querystring:
			url += '?{}'.format(querystring)
		return url

	def alive(self):
		url = self.__build_url('ping')
		try:
			response = requests.get(url)
		except Exception, e:
			return False
		if response.status_code != 200:
			return False
		return True

	def challenges(self):
		url = self.__build_url('challenges')
		response = requests.get(url)
		if response.status_code != 200:
			raise MapRouletteServerException('server did not return challenges')
		return response.json()

	def get(self, endpoint, querystring=None, replacements=None):
		url = self.__build_url(
			endpoint,
			querystring=querystring,
			replacements=replacements)
		response = requests.get(url)
		if response.status_code != 200:
			raise MapRouletteServerException('server did not return OK from {}'.format(url))
		return response.json()

	def post(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		response = requests.post(url, json=payload)
		if response.status_code != 201:
			raise MapRouletteServerException('server did not return OK from {}'.format(url))
		return response.json()

	def put(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		response = requests.put(url, json=payload)
		if response.status_code != 200:
			raise MapRouletteServerException('server did not return OK from {}'.format(url))
		return response.json()

class MapRouletteServerException(Exception):
	"""oops, something went wrong while interacting with the server"""

	def __init__(self, message):
		super(MapRouletteServerException, self).__init__(self, message)