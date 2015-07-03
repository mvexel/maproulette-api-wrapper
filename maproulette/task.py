#!/usr/bin/env python


class MapRouletteTask(Object):
	"""A task for MapRoulette"""

    instruction = None
    geometries = None
    status = None

	def __init__(self):
		pass

    def create(self):
        """Create the task on the server"""

        pass

    def update(self):
        """Update existing task on the server"""

        pass

    def retrieve(self):
        """Retrieve a task from the server"""

        pass

    def as_payload(self):
        return {
            key:value for key, value in self.__dict__.items()
            if not key.startswith('__') and not callable(key)}


class MapRouletteTaskCollection(Object):
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