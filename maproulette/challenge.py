#!/usr/bin/env python

class MapRouletteChallenge(object):
	"""A challenge for MapRoulette"""

	slug = None
	title = None
	active = False
	blurb = ''
	help = ''
	instruction = ''
	description = ''
	difficulty = 2
	type = None

	def __init__(
		self,
		slug,
		title,
		active=None,
		blurb=None,
		help=None,
		instruction=None,
		description=None,
		difficulty=None,
		type=None):
		self.slug = slug
		self.title = title
		if active:
			self.active = active
		if blurb:
			self.blurb = blurb
		if help:
			self.help = help
		if description:
			self.description = description
		if difficulty:
			self.difficulty = difficulty

	def create(self, server):
		"""Create the challenge on the server"""
		return server.post(
			'challenge_admin',
			self.as_payload(),
			replacements={'slug': self.slug})

	def update(self, server):
		"""Update existing challenge on the server"""
		return server.put(
			'challenge_admin',
			self.as_payload(),
			replacements={'slug': self.slug})

	def retrieve(self, server):
		"""Retrieve challenge from the server"""
		challenge = server.get(
			'challenge',
			replacements={'slug': self.slug})
		pass

	def as_payload(self):
		return {
			key:value for key, value in self.__dict__.items()
			if not key.startswith('__') and not callable(key)}

	@classmethod
	def from_server(cls, server, slug):
		challenge = server.get(
			'challenge',
			replacements={'slug': slug})
		if not challenge['status_code'] == 200:
			return False
		return cls(
			**challenge['response'])