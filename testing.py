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


if __name__ == '__main__':
    unittest.main()
