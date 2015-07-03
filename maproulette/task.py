#!/usr/bin/env python


class MapRouletteTask(object):
	"""A task for MapRoulette"""

	instruction = ''
	geometries = None
	status = None
	__challenge__ = None
	__identifier__ = None

	def __init__(
		self,
		challenge,
		identifier,
		instruction=None,
		geometries=None,
		status=None):
		self.__challenge__ = challenge
		self.__identifier__ = identifier
		if instruction:
			self.instruction = instruction
		if geometries:
			self.geometries = geometries
		if status:
			self.status = status

	def create(self, server):
		"""Create the task on the server"""
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

	def as_payload(self):
		return {
			key:value for key, value in self.__dict__.items()
			if not key.startswith('__')
			and not callable(key)}

	@classmethod
	def from_server(cls, server, slug):
		task = server.get(
			'task',
			replacements={
				'slug': self.__challenge__.slug,
				'identifier': self.__identifier__})
		if not task['status_code'] == 200:
			return False
		return cls(
			**task['response'])

class MapRouletteTaskCollection(object):
	"""A collection of tasks for MapRoulette"""

	def __init__(self):
		pass

	def create(self):
		"""Create the tasks on the server"""

		pass

	def update(self):
		"""Update existing tasks on the server"""

		pass

	def retrieve(self):
		"""Retrieve tasks from the server"""

		pass


	def as_payload(self):
		pass