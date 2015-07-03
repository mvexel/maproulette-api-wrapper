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
		'ping'	  		 : '/ping',
		'challenges'	 : '/challenges',
		'challenge'	 	 : '/challenge/{slug}',
		'challenge_admin': '/admin/challenge/{slug}',
		'tasks_admin'	 : '/admin/challenge/{slug}/tasks'
	}

	base_url = ''

	def __init__(self, instance='local'):
		self.base_url = self.SERVERS[instance]


	def __server_message(self, response):
		r = None
		try:
			r = response.json()
		except ValueError, e:
			r = {'message': response.text}
		return dict(
			status_code=response.status_code,
			response=r)

	def __build_url(self, endpoint, querystring=None, replacements=None):
		if not endpoint in self.ENDPOINTS:
			return None
		url = self.base_url
		if replacements:
			url += self.ENDPOINTS[endpoint].format(**replacements)
		else:
			url += self.ENDPOINTS[endpoint]
		if querystring:
			url += '?{}'.format(querystring)
		return url

	def alive(self):
		response = requests.get(self.base_url + self.ENDPOINTS['ping'])
		if not response.ok:
			return False
		return True

	def challenges(self):
		response = requests.get(self.base_url + '/challenges')
		return self.__server_message(response)

	def get(self, endpoint, querystring=None, replacements=None):
		url = self.__build_url(
			endpoint,
			querystring=querystring,
			replacements=replacements)
		if not url:
			return None
		response = requests.get(url)
		return self.__server_message(response)

	def post(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		if not url:
			return None
		response = requests.post(url, json=payload)
		return self.__server_message(response)

	def put(self, endpoint, payload, replacements=None):
		url = self.__build_url(
			endpoint,
			replacements=replacements)
		if not url:
			return None
		response = requests.put(url, json=payload)
		return self.__server_message(response)