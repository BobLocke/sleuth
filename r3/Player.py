#-------------------------------------------------------------------------------
# Name:        Player
# Purpose:
#
# Author:      r.dean
#
# Created:     09/11/2012
# Copyright:   (c) r.dean 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

suspects = {"Mrs. White": (0, 9),
            "Mr. Green": (0, 14),
            "Miss Scarlet": (24, 8),
            "Professor Plum": (19,23),
            "Colonel Mustard": (17,0),
            "Ms. Peacock": (6,23)}

class Player:
    def __init__(self, character):
        self.character = character
        self.position = suspects[character]
        self.hand = set()

    def addCard(self, card):
        self.hand.add(card)
