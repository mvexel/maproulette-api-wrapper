#!/usr/bin/env python

class MapRouletteChallenge(object):
	"""A challenge for MapRoulette"""

	slug = None
	title = None
	active = None
	blurb = None
	help = None
	instruction = None
	description = None
	difficulty = None
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
		self.active = active or False
		self.blurb = blurb or ''
		self.help = help or ''
		self.description = description or ''
		self.difficulty = difficulty or 2

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

	def exists(self, server):
		"""Check if a challenge exists on the server"""
		try:
			response = server.get(
				'challenge',
				replacements={'slug': self.slug})
		except Exception:
			return False
		return True

	def as_payload(self):
		return {
			key:value for key, value in self.__dict__.items()
			if not key.startswith('__')
			and not value is None
			and not callable(key)}

	@classmethod
	def from_server(cls, server, slug):
		challenge = server.get(
			'challenge',
			replacements={'slug': slug})
		return cls(
			**challenge)