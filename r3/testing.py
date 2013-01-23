#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      r.dean
#
# Created:     02/08/2012
# Copyright:   (c) r.dean 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from sleuth import Sleuth
from  GameBoard import GameBoard
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        self.s = Sleuth(["Mr. Green", "Professor Plum", "Miss Scarlet"])

    def test_uniquehands(self):
        rebuiltdeck = []
        rebuiltdeck += self.s.solution
        for x in self.s.players:
            rebuiltdeck += x.hand
        assert len(rebuiltdeck) == len(set(rebuiltdeck))

    def test_equalhands(self):
        for l in [len(p.hand) for p in self.s.players]:
            for x in self.s.players:
                assert abs(len(x.hand) - l) <= 1

    def test_solutionLen(self):
        assert len(self.s.solution) == 3

    def test_solutionUnique(self):
        t = {x.catagory for x in self.s.solution}
        assert t == {"w", "r", "s"}

    def test_basicMove(self):
        g = GameBoard()
        position = (17, 3)
        roll = 3
        landings = g.move(position, roll, position)
        assert landings == ((16, 3), (18, 3), (17, 4), (17, 2), (16, 5), (18, 5), (17, 6))


if __name__ == '__main__':
    unittest.main()
