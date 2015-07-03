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

## Tests

`python run_tests.py`
