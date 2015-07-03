#!/usr/bin/env python

import unittest
import uuid
from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge

class ServerTests(unittest.TestCase):

	def test_init(self):
		server = MapRouletteServer()
		self.assertTrue(isinstance(server, MapRouletteServer))

	def test_challenges(self):
		server = MapRouletteServer()
		challenges = server.challenges()
		self.assertTrue(
			challenges['status_code'] == 200 and
			isinstance(challenges['response'], list))


class ChallengeTests(unittest.TestCase):

	test_challenge_slug = 'test-{}'.format(uuid.uuid4())

	def test_create_challenge(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge'
		)
		response = challenge.create(server)
		self.assertTrue(
			response['status_code'] == 201)

	def test_retrieve_challenge(self):
		server=MapRouletteServer()
		challenge = MapRouletteChallenge.from_server(
			server,
			self.test_challenge_slug)

	def test_update_challenge(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge Updated',
			active=True
		)
		response = challenge.update(server)
		self.assertTrue(
			response['status_code'] == 200)


if __name__ == '__main__':
	unittest.main()