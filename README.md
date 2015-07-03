# maproulette-api-wrapper

A python wrapper for the MapRoulette API

## Install

`pip install maproulette`

## Usage

### Create a challenge

```[python]
from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge
server = MapRouletteServer()
challenge = MapRouletteChallenge(
	slug='my_challenge',
	title='My Challenge')
response = challenge.create(server)
```

### Create a task

```[python]
from maproulette.server import MapRouletteServer
from maproulette.challenge import MapRouletteChallenge
from maproulette.task import MapRouletteTask
server = MapRouletteServer()
challenge = MapRouletteChallenge.from_server(
	server,
	'my_challenge')
task = MapRouletteTask(
	challenge,
	'my-task-identifier')
response = task.create(server)
```

## Tests

`python run_tests.py`
