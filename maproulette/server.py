#!/usr/bin/env python

"""
A MapRoulette server.
"""

import requests
import json

class MapRouletteServer(object):
	"""
	Typical usage::

		server = MapRouletteServer(
			url='http://dev.maproulette.org/api')

	:param url: The URL for the MapRoulette API server you want to use
	:type url: String
	:rtype: A :py:class:`MapRouletteServer`
	"""

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

	def __init__(self, url):
		self.base_url = url
		if not self.alive():
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
			raise Exception('server did not return challenges')
		return response.json()

	def get(self, endpoint, querystring=None, replacements=None):
		url = self.__build_url(
			endpoint,
			querystring=querystring,
			replacements=replacements)
		response = requests.get(url)
		if response.status_code != 200:
			raise Exception('server did not return OK from {}'.format(url))
		return response.json()

	def post(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		response = requests.post(url, json=payload)
		if response.status_code != 201:
			raise Exception('server did not return OK from {}'.format(url))
		return response.json()

	def put(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		response = requests.put(url, json=payload)
		if response.status_code != 200:
			raise Exception('server did not return OK from {}'.format(url))
		return response.json()