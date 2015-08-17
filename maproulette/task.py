#!/usr/bin/env python

"""
A task for MapRoulette.
"""


class MapRouletteTask(object):
    """
    Typical usage::

        task = MapRouletteTask(
            identifier,
            challenge=challenge,
            geometries=geometries,
            instruction=instruction)
        task.create(server_instance)

    :param identifier: A valid Task identifier
    :param challenge: An instance of MapRouletteChallenge
    :param geometries: One or more geometries serialized as a GeoJSON FeatureCollection
    :type geometries: FeatureCollection
    :param instruction: A task-level instruction
    :param status: The task's initial status (defaults to 'created' in MapRoulette)
    """
    instruction = None
    geometries = None
    status = None
    __challenge__ = None
    identifier = None

    def __init__(
            self,
            identifier,
            challenge=None,
            geometries=None,
            instruction=None,
            status=None):
        self.__challenge__ = challenge
        self.identifier = identifier
        self.geometries = geometries
        self.instruction = instruction or ''
        self.status = status or None

    def create(self, server):
        """Create the task on the server"""
        if len(self.geometries) == 0:
            raise Exception('no geometries')
        return server.post(
            'task_admin',
            self.as_payload(),
            replacements={
                'slug': self.__challenge__.slug,
                'identifier': self.identifier})

    def update(self, server):
        """Update existing task on the server"""
        return server.put(
            'task_admin',
            self.as_payload(),
            replacements={
                'slug': self.__challenge__.slug,
                'identifier': self.identifier})

    def exists(self, server):
        """Check if a task exists on the server"""
        try:
            server.get(
                'task',
                replacements={
                    'slug': self.__challenge__.slug,
                    'identifier': self.identifier})
        except Exception:
            return False
        return True

    def as_payload(self, with_identifier=False):
        payload = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('__')
            and not value is None
            and not callable(key)}
        if with_identifier:
            payload['identifier'] = self.identifier
        return payload

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    @classmethod
    def from_server(cls, server, slug, identifier):
        """Retrieve a task from the server"""
        task = server.get(
            'task',
            replacements={
                'slug': slug,
                'identifier': identifier})
        return cls(**task)

    @classmethod
    def from_payload(cls, payload):
        """Create a task from JSON"""
        return cls(**payload)
