#!/usr/bin/env python

import json
from maproulette.challenge import MapRouletteChallenge

class MapRouletteTask(object):
	"""
	A task for MapRoulette

	Typical usage::

		task = MapRouletteTask(
			challenge=challenge_obj,
			identifier=identifier,
			geometries=geometries)
		task.create(server_instance)
		
	:param challenge: An instance of MapRouletteChallenge
	:param identifer: A valid Task identifer
	:param geometries: One or more geometries serialized as a GeoJSON FeatureCollection
	:type geometries: FeatureCollection
	:param instruction: A task-level instruction
	:param status: The task's initial status (defaults to 'created' in MapRoulette)
	"""
	instruction = None
	geometries = None
	status = None
	__challenge__ = None
	__identifier__ = None

	def __init__(
		self,
		challenge,
		identifier,
		geometries,
		instruction=None,
		status=None):
		self.__challenge__ = challenge
		self.__identifier__ = identifier
		self.geometries = geometries
		self.instruction = instruction or ''
		self.status = status or None

	def create(self, server):
		"""Create the task on the server"""
		if len(self.geometries) == 0:
			raise MapRouletteTaskException('no geometries')
		return server.post(
			'task_admin',
			self.as_payload(),
			replacements={
				'slug': self.__challenge__.slug,
				'identifier': self.__identifier__})

	def update(self):
		"""Update existing task on the server"""
		return server.put(
			'task_admin',
			self.as_payload(),
			replacements={
				'slug': self.__challenge__.slug,
				'identifier': self.__identifier__})

	def add(self, task):
		self.tasks.append(task)

	def as_payload(self, with_identifier=False):
		payload = {
			key:value for key, value in self.__dict__.items()
			if not key.startswith('__')
			and not value is None
			and not callable(key)}
		if with_identifier:
			payload['identifier'] = self.__identifier__
		return payload

	@classmethod
	def from_server(cls, server, slug):
		task = server.get(
			'task',
			replacements={
				'slug': self.__challenge__.slug,
				'identifier': self.__identifier__})
		return cls(**task)


class MapRouletteTaskCollection(object):
	"""A collection of tasks for MapRoulette"""

	MAX_TASKS = 5000
	tasks = None
	__challenge__ = None

	def __init__(self, challenge, tasks=None):
		if not isinstance(challenge, MapRouletteChallenge):
			raise MapRouletteTaskException('challenge is not a challenge')
		self.__challenge__ = challenge
		self.tasks = tasks or []

	def create(self, server):
		"""Create the tasks on the server"""
		for chunk in self.__cut_to_size():
			server.post(
				'tasks_admin',
				chunk.as_payload(),
				replacements={
					'slug': chunk.__challenge__.slug})

	def update(self, server):
		"""Update existing tasks on the server"""
		for chunk in self.__cut_to_size():
			server.put(
				'tasks_admin',
				chunk.as_payload(),
				replacements={
					'slug': chunk.__challenge__.slug})

	def as_payload(self):
		payload = [
			task.as_payload(with_identifier=True)
			for task in self.tasks]
		return payload

	def __cut_to_size(self):
		return (
			MapRouletteTaskCollection(
				self.__challenge__,
				tasks=self.tasks[i:i+self.MAX_TASKS])
			for i in xrange(0, len(self.tasks), self.MAX_TASKS))


class MapRouletteTaskException(Exception):
	"""A task is not kosher"""

	def __init__(self, message):
		super(MapRouletteTaskException, self).__init__(self, message)