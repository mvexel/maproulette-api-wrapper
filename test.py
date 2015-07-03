#!/usr/bin/env python

import unittest
from maproulette.server import MapRouletteServer

class ServerTests(unittest.TestCase):

    def test_init_server(self):
        server = MapRouletteServer()
        self.assertTrue(isinstance(server, MapRouletteServer))

if __name__ == '__main__':
    unittest.main()