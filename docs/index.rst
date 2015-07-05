.. MapRoulette API Wrapper documentation master file, created by
   sphinx-quickstart on Sun Jul  5 11:58:01 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MapRoulette API Wrapper
***********************

This project provides a convenient wrapper around the `MapRoulette API`_. You can create and maintain Challenges and Tasks on a local MapRoulette server or on the main MapRoulette `dev`_ and `production`_ servers.

.. _MapRoulette API: https://github.com/osmlab/maproulette/wiki/API-Documentation
.. _dev: http://dev.maproulette.org/
.. _production: http://maproulette.org/


Installation
============

See `the project README`_

.. _the project README: https://github.com/mvexel/maproulette-api-wrapper/blob/master/README.md

Prepare a challenge
===================

You need a few things to create your own MapRoulette challenge: 

* Challenge metadata. At the very least you need a `title`_, a `slug`_ and some instructions to show the user.
* Tasks. 
* Access to a server. It is recommended that you try your challenge on a `local development server`_ first, then move on to the main MapRoulette servers.

.. _local development server: https://github.com/osmlab/maproulette/wiki/Run-A-MapRoulette-Development-Server-Locally
.. _slug: https://github.com/osmlab/maproulette/wiki/Challenge-Style-Guide#challenge-slug
.. _title: https://github.com/osmlab/maproulette/wiki/Challenge-Style-Guide#challenge-title

Once you have those things, you can get to work!

First, we get a MapRoulette server instance::

	from maproulette import MapRouletteServer
	server = MapRouletteServer()

Without any arguments, this will get a :class:`MapRouletteServer` instance that points at a local MapRoulette development server at ``http://localhost:5000``. 

Next, we create a new Challenge on this server::

	from maproulette import MapRouletteChallenge
	challenge = MapRouletteChallenge(
		slug='test-challenge',
		title='Test Challenge')
	challenge.create(server)

Finally, let's prepare a task and add it to the challenge::

	from maproulette import MapRouletteTask
	from geojson import FeatureCollection, Feature, Point
	task = MapRouletteTask(
	    challenge,
	    identifier='test-task-1',
	    geometries=FeatureCollection([Feature(
		    geometry=Point((random(), random())))]))
	task.create(server))

See how we use :class:`geojson.FeatureCollection`, :class:`geojson.Feature` and :class:`geojson.Point` to generate a GeoJSON geometry on the fly. In real life, you would probably get these from another source. Note that MapRoulette requires the task geometry to be wrapped in a FeatureCollection, even if the geometry is just a single point, like in the example above.

You can also use :class:`MapRouletteTaskCollection` to create multiple tasks at once.

API
***

MapRoulette Server
==================

.. automodule:: maproulette.server
	:members:

MapRoulette Challenge
=====================

.. automodule:: maproulette.challenge
	:members:

MapRoulette Task
================

.. automodule:: maproulette.task
	:members:
