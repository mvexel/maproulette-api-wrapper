#!/usr/bin/env python

import unittest
import uuid
from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge
from maproulette.task import MapRouletteTask, MapRouletteTaskCollection
from geojson import FeatureCollection, Feature, Point
from random import random

class APITests(unittest.TestCase):

	test_challenge_slug = 'test-{}'.format(uuid.uuid4())
	test_task_identifier = 'task-{}'.format(uuid.uuid4())

	def test_init(self):
		server = MapRouletteServer()
		self.assertTrue(isinstance(server, MapRouletteServer))

	def test_challenges(self):
		server = MapRouletteServer()
		challenges = server.challenges()
		self.assertTrue(isinstance(challenges, list))

	def test_01_create_challenge(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge'
		)
		self.assertFalse(challenge.exists(server))
		response = challenge.create(server)
		self.assertTrue(challenge.exists(server))

	def test_02_retrieve_challenge(self):
		server=MapRouletteServer()
		challenge = MapRouletteChallenge.from_server(
			server,
			self.test_challenge_slug)

	def test_03_update_challenge(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge Updated',
			active=True
		)
		response = challenge.update(server)

	def test_04_create_task(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge.from_server(
			server,
			self.test_challenge_slug)
		task = MapRouletteTask(
			challenge,
			identifier=self.test_task_identifier,
			geometries=self.__random_point())
		response = task.create(server)

	def test_05_task_exists(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge.from_server(
			server,
			self.test_challenge_slug)
		task = MapRouletteTask(
			challenge,
			identifier=self.test_task_identifier,
			geometries=self.__random_point())
		self.assertTrue(task.exists(server))


	def test_06_create_a_ton_of_tasks(self):
		server = MapRouletteServer()
		challenge = MapRouletteChallenge.from_server(
			server,
			self.test_challenge_slug)
		task_collection = MapRouletteTaskCollection(challenge)
		i = 0
		while i < 100:
			i += 1
			task_collection.tasks.append(
				MapRouletteTask(
					challenge,
					identifier='task-{}'.format(uuid.uuid4()),
					geometries=self.__random_point()))
		response = task_collection.create(server)

	def __random_point(self):
		return FeatureCollection([
			Feature(geometry=Point((random(), random())))])

if __name__ == '__main__':
	unittest.main()