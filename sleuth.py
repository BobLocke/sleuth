#-------------------------------------------------------------------------------
# Name:        sleuth
# Purpose:
#
# Author:      r.dean
#
# Created:     09/08/2012
# Copyright:   (c) r.dean 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from itertools import cycle
from random import shuffle

from Player import Player
from GameBoard import GameBoard

weaponCards = [("Lead Pipe", "w"), ("Candlestick", "w"), ("Revolver", "w"), ("Rope" , "w"), ("Knife", "w"), ("Wrench", "w")]
roomCards = [("Conservatory", "r"), ("Kitchen", "r"), ("Billards Room", "r"), ("Ballroom","r"), ("Hall","r"), ("Dining Room","r"), ("Study","r"), ("Lounge", "r"), ("Library", "r")]
suspectCards = [("Mrs. White", "s"), ("Mr. Green", "s"), ("Miss Scarlet","s"), ("Professor Plum","s"), ("Colonel Mustard","s"), ("Ms. Peacock","s")]
suspects = ["Mr. Green", "Professor Plum", "Miss Scarlet"]  # DEBUG


class Sleuth(object):
    _board = GameBoard()

    def __init__(self, suspects):
        self.player_count = len(suspects)
        self.players = [Player(s) for s in suspects]
        deck = Deck()
        self.solution = deck.solution
        deck.deal(self.players)

    @classmethod
    def board(cls):
        return cls._board


class Room(object):
    def __init__(self, neighbors, room_name):
        self.name = room_name


class Card (object):
    def __init__(self, name, catagory):
        self.name = name
        self.catagory = catagory

    def __str__(self):
        return self.name


class Deck(object):
    def __init__(self):
        self.weaponCards = [Card(arg1, arg2) for arg1, arg2 in weaponCards]
        self.roomCards = [Card(arg1, arg2) for arg1, arg2 in roomCards]
        self.suspectCards = [Card(arg1, arg2) for arg1, arg2 in suspectCards]
        shuffle(self.weaponCards)
        shuffle(self.suspectCards)
        shuffle(self.roomCards)
        self.solution = self.solution()
        self.deck = self.buildDeck()

    def buildDeck(self):
        return (self.weaponCards + self.suspectCards + self.roomCards)

    def solution(self):
        return {self.weaponCards.pop(),
                self.roomCards.pop(),
                self.suspectCards.pop()}

    def deal(self, players):
        for player, card in zip(cycle(players), self.deck):
            player.addCard(card)
