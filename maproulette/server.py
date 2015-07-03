#!/usr/bin/env python

class MapRouletteServer(Object):
	"""A MapRoulette server"""

    MAPROULETTE_PRODUCTION_URL = 'http://maproulette.org/'

    base_url = ''

	def __init__(self, url=MAPROULETTE_PRODUCTION_URL):
		self.base_url = url
