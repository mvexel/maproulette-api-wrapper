#!/usr/bin/env python

import unittest
import uuid
from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge
from maproulette.task import MapRouletteTask
from maproulette.taskcollection import MapRouletteTaskCollection
from geojson import FeatureCollection, Feature, Point
from random import random

class APITests(unittest.TestCase):

	A_TON = 100

	test_challenge_slug = 'test-{}'.format(uuid.uuid4())
	test_task_identifier = 'task-{}'.format(uuid.uuid4())
	test_server_url = 'http://localhost:5000/api'
	server = MapRouletteServer(url=test_server_url)

	def test_001_init(self):
		self.assertTrue(isinstance(self.server, MapRouletteServer))

	def test_002_challenges(self):
		challenges = self.server.challenges()
		self.assertTrue(isinstance(challenges, list))

	def test_003_create_challenge(self):
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge'
		)
		self.assertFalse(challenge.exists(self.server))
		response = challenge.create(self.server)
		self.assertTrue(challenge.exists(self.server))

	def test_004_retrieve_challenge(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)

	def test_005_update_challenge(self):
		challenge = MapRouletteChallenge(
			slug=self.test_challenge_slug,
			title='Test Challenge Updated',
			active=True
		)
		response = challenge.update(self.server)

	def test_006_create_task(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)
		task = MapRouletteTask(
			challenge=challenge,
			identifier=self.test_task_identifier,
			geometries=self.__random_point())
		response = task.create(self.server)

	def test_007_task_exists(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)
		task = MapRouletteTask(
			challenge=challenge,
			identifier=self.test_task_identifier,
			geometries=self.__random_point())
		self.assertTrue(task.exists(self.server))

	def test_008_create_a_ton_of_tasks(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)
		task_collection = self.__create_task_collection(challenge)
		response = task_collection.create(self.server)

	def test_009_retrieve_taskcollection_from_server(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)
		task_collection = MapRouletteTaskCollection.from_server(
			self.server,
			challenge)
		self.assertTrue(len(task_collection.tasks) == self.A_TON + 1)
		# We already created 1 task in test 006, then A_TON more in test 008

	def test_010_reconcile_task_collections(self):
		challenge = MapRouletteChallenge.from_server(
			self.server,
			self.test_challenge_slug)
		task_collection = MapRouletteTaskCollection.from_server(
			self.server,
			challenge)
		# remove the last task, so it appears 'deleted'
		task_collection.tasks.pop()
		# append a different task in place, so it appears 'new'
		task_collection.tasks.append(
			MapRouletteTask(
				challenge=challenge,
				identifier='task-{}'.format(uuid.uuid4()),
				geometries=self.__random_point()))
		task_collection.reconcile(self.server)

	def __random_point(self):
		return FeatureCollection([
			Feature(geometry=Point((random(), random())))])

	def __create_task_collection(self, challenge):
		task_collection = MapRouletteTaskCollection(challenge)
		i = 0
		while i < self.A_TON:
			i += 1
			task_collection.tasks.append(
				MapRouletteTask(
					challenge=challenge,
					identifier='task-{}'.format(uuid.uuid4()),
					geometries=self.__random_point()))
		return task_collection

if __name__ == '__main__':
	unittest.main()