#!/usr/bin/env python

"""
A collection of Tasks
"""

from .challenge import MapRouletteChallenge
from .task import MapRouletteTask

class MapRouletteTaskCollection(object):
	"""A collection of tasks for MapRoulette."""

	MAX_TASKS = 5000
	tasks = None
	challenge = None

	def __init__(
		self,
		challenge,
		tasks=None):
		if challenge and not isinstance(challenge, MapRouletteChallenge):
			raise Exception('challenge is not a MapRouletteChallenge')
		self.challenge = challenge
		self.tasks = tasks or []

	def create(self, server):
		"""Create the tasks on the server"""
		for chunk in self.__cut_to_size():
			server.post(
				'tasks_admin',
				chunk.as_payload(),
				replacements={
					'slug': chunk.challenge.slug})

	def update(self, server):
		"""Update existing tasks on the server"""
		for chunk in self.__cut_to_size():
			server.put(
				'tasks_admin',
				chunk.as_payload(),
				replacements={
					'slug': chunk.challenge.slug})

	def reconcile(self, server):
		"""
		Reconcile this collection with the server.
		"""
		if not self.challenge.exists(server):
			raise Exception('Challenge does not exist on server')
		existing = MapRouletteTaskCollection.from_server(server, self.challenge)
		for task in self.tasks:
			if task.identifier in [task.identifier for task in existing.tasks]:
				print 'exists'
			else:
				print 'new'
		for task in existing.tasks:
			if task.identifier not in [task.identifier for task in self.tasks]:
				print 'delete'


	def add(self, server):
		"""Add task colleciton to the Collection."""
		self.tasks.append(task)

	def as_payload(self):
		payload = [
			task.as_payload(with_identifier=True)
			for task in self.tasks]
		return payload

	def __cut_to_size(self):
		return (
			MapRouletteTaskCollection(
				self.challenge,
				tasks=self.tasks[i:i+self.MAX_TASKS])
			for i in xrange(0, len(self.tasks), self.MAX_TASKS))

	@classmethod
	def from_server(cls, server, challenge):
		if not challenge.exists(server):
			raise Exception('challenge does not exist on server')
		tasks = []
		response = server.get(
			'tasks_admin',
			replacements={'slug': challenge.slug})
		for task in response:
			tasks.append(MapRouletteTask.from_payload(task))
		return cls(challenge, tasks=tasks)