#!/usr/bin/env python

"""
A collection of tasks for MapRoulette.
This is not a native MapRoulette object, but rather a convenience object
to leverage the bulk insert / update calls in the MapRoulette API. The 
MapRouletteTaskCollection class contains one notable method that is not native
to the MapRoulette API: :py:func:`.reconcile`, which reconciles a task collection
with the corresponding challenge on the server.
"""

from .challenge import MapRouletteChallenge
from .task import MapRouletteTask
from past.builtins import xrange


class MapRouletteTaskCollection(object):
    """
    Typical usage::

        task_collection = MapRouletteTaskCollection(
            challenge=challenge_obj,
        task_collection.append(task)
        task_collection.create(server)

    :param challenge: An instance of MapRouletteChallenge
    """

    MAX_TASKS = 1000
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

        same = []
        new = []
        changed = []
        deleted = []

        # reconcile the new tasks with the existing tasks:
        for task in self.tasks:
            # if the task exists on the server...
            if task.identifier in [existing_task.identifier for existing_task in existing.tasks]:
                # and they are equal...
                if task == existing.get_by_identifier(task.identifier):
                    # add to 'same' list
                    same.append(task)
                    # if they are not equal, add to 'changed' list
                else:
                    changed.append(task)
            # if the task does not exist on the server, add to 'new' list
            else:
                new.append(task)

        # next, check for tasks on the server that don't exist in the new collection...
        for task in existing.tasks:
            if task.identifier not in [task.identifier for task in self.tasks]:
                # ... and add those to the 'deleted' list.
                deleted.append(task)

        # update the server with new, changed, and deleted tasks
        if new:
            newCollection = MapRouletteTaskCollection(self.challenge, tasks=new)
            newCollection.create(server)
        if changed:
            changedCollection = MapRouletteTaskCollection(self.challenge, tasks=changed)
            changedCollection.update(server)
        if deleted:
            deletedCollection = MapRouletteTaskCollection(self.challenge, tasks=deleted)
            for task in deletedCollection.tasks:
                task.status = 'deleted'
            deletedCollection.update(server)
        # return same, new, changed and deleted tasks
        return {'same': same, 'new': new, 'changed': changed, 'deleted': deleted}

    def add(self, task):
        """Add task colleciton to the Collection."""
        self.tasks.append(task)

    def get_by_identifier(self, identifier):
        return next((task for task in self.tasks if task.identifier == identifier), None)

    def as_payload(self):
        payload = [
            task.as_payload(with_identifier=True)
            for task in self.tasks]
        return payload

    def __cut_to_size(self):
        return (
            MapRouletteTaskCollection(
                self.challenge,
                tasks=self.tasks[i:i + self.MAX_TASKS])
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
