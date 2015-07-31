#!/usr/bin/env python

"""
A challenge for MapRoulette.
"""


class MapRouletteChallenge(object):
    """
    Typical usage::

        challenge = MapRouletteChallenge(
            slug=slug,
            title=title)
        challenge.create(server_instance)

    :param slug: A valid slug for this challenge
    :param title: Challenge title
    :type title: String
    :param active: Whether the challenge should be active or not
    :type active: Boolean
    :param blurb: A sort blurb describing the challenge
    :param help: Help text for the challenge
    :param instruction: Challenge-level instruction text
    :param description: A longer description text for the challenge
    :param difficulty: Challenge difficulty level (1-3)
    :rtype: A :class:`MapRouletteChallenge`

    """
    slug = None
    title = None
    active = None
    blurb = None
    help = None
    instruction = None
    description = None
    difficulty = None
    type = None

    def __init__(
            self,
            slug,
            title,
            active=None,
            blurb=None,
            help=None,
            instruction=None,
            description=None,
            difficulty=None,
            type=None):
        self.slug = slug
        self.title = title
        self.active = active or False
        self.blurb = blurb or ''
        self.help = help or ''
        self.description = description or ''
        self.difficulty = difficulty or 2

    def create(self, server):
        """Create the challenge on the server"""

        return server.post(
            'challenge_admin',
            self.as_payload(),
            replacements={'slug': self.slug})

    def update(self, server):
        """Update existing challenge on the server"""

        return server.put(
            'challenge_admin',
            self.as_payload(),
            replacements={'slug': self.slug})

    def delete(self, server):
        return server.delete(
            'challenge_admin',
            replacements={'slug': self.slug}
        )

    def exists(self, server):
        """Check if a challenge exists on the server"""

        try:
            server.get(
                'challenge',
                replacements={'slug': self.slug})
        except Exception:
            return False
        return True

    def as_payload(self):
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('__')
            and value is not None
            and not callable(key)}

    @classmethod
    def from_server(cls, server, slug):
        """Retrieve a challenge from the MapRoulette server
        :type server
        """

        challenge = server.get(
            'challenge',
            replacements={'slug': slug})
        return cls(
            **challenge)
