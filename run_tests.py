#!/usr/bin/env python

import unittest
import uuid
from random import random
import os
import sys

from geojson import FeatureCollection, Feature, Point

from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge
from maproulette.task import MapRouletteTask
from maproulette.taskcollection import MapRouletteTaskCollection


class APITests(unittest.TestCase):
    # how much is A_TON?
    A_TON = 100
    test_challenge_slug = 'test-{}'.format(uuid.uuid4())
    test_task_identifier = 'task-{}'.format(uuid.uuid4())
    test_server_url = os.environ.get("MAPROULETTE_API_SERVER")
    test_credentials = {
        'user': os.environ.get("MAPROULETTE_API_USER"),
        'password': os.environ.get("MAPROULETTE_API_PASSWORD")}
    server = MapRouletteServer(
        url=test_server_url,
        user=test_credentials['user'],
        password=test_credentials['password'])

    def test_001_init(self):
        """
        Assert that the server is indeed alive.
        """
        self.assertTrue(isinstance(self.server, MapRouletteServer))

    def test_002_challenges(self):
        """
        Assert that the server returns a list of challenges
        """
        challenges = self.server.challenges()
        self.assertTrue(isinstance(challenges, list))

    def test_003_create_challenge(self):
        challenge = MapRouletteChallenge(
            slug=self.test_challenge_slug,
            title='Test Challenge'
        )
        self.assertFalse(challenge.exists(self.server))
        challenge.create(self.server)
        self.assertTrue(challenge.exists(self.server))

    def test_004_retrieve_challenge(self):
        MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)

    def test_005_update_challenge(self):
        challenge = MapRouletteChallenge(
            slug=self.test_challenge_slug,
            title='Test Challenge Updated',
            active=True
        )
        challenge.update(self.server)

    def test_006_create_task(self):
        challenge = MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)
        task = MapRouletteTask(
            challenge=challenge,
            identifier=self.test_task_identifier,
            geometries=self.__random_point())
        task.create(self.server)

    def test_007_task_exists(self):
        challenge = MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)
        task = MapRouletteTask(
            challenge=challenge,
            identifier=self.test_task_identifier)
        print task
        self.assertTrue(task.exists(self.server))

    def test_008_create_a_ton_of_tasks(self):
        challenge = MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)
        task_collection = self.__create_task_collection(challenge)
        task_collection.create(self.server)

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
        """
        In this test case, we will reconcile a task collection with an
        existing one on the server (created in 008).
        Compared to the existing task collection, we will remove one task,
        add one task, and change one task.
        """

        # get the challenge from server
        challenge = MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)
        # get the task collection to reconcile, start out with the
        # existing one on the server
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
        # and finally change one task so it appears 'updated'
        task_collection.tasks[0].geometries = self.__random_point()
        task_collection.tasks[0].status = 'changed'

        # reconcile the two collections
        result = task_collection.reconcile(self.server)

        # assert that we indeed have one new, one changed and one deleted task.
        self.assertTrue(len(result['new']) == 1)
        self.assertTrue(len(result['changed']) == 1)
        self.assertTrue(len(result['deleted']) == 1)

    def test_011_delete_challenge(self):
        """
        Delete the challenge that was created for this test
        """

        # get the challenge from server
        challenge = MapRouletteChallenge.from_server(
            self.server,
            self.test_challenge_slug)
        challenge.delete(self.server)


    def __random_point(self):
        self.geometries__ = """
        return a random geographic Point, wrapped in a Feature, wrapped in a
        FeatureCollection. It's like the Turducken of geometries.
        """
        return FeatureCollection([
            Feature(geometry=Point((random(), random())))])

    def __create_task_collection(self, challenge):
        """
        Return a collection of A_TON of tasks with random Point geometries
        """
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
    if not os.environ.get("MAPROULETTE_API_USER"):
        print("Please set MAPROULETTE_API_USER environment variable")
        if not os.environ.get("MAPROULETTE_API_PASSWORD"):
            print("Please set MAPROULETTE_API_PASSWORD environment variable")
            sys.exit()
    unittest.main()
