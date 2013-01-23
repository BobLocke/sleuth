#-------------------------------------------------------------------------------
# Name:        deck
# Purpose: A deck of the cards used in the board game "Sleuth"
#
# Author:      r.dean
#
# Created:     02/08/2012
# Copyright:   (c) r.dean 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

clueCards = [("Conservatory" , "r"), ("Lead Pipe", "w"), ("Candlestick", "w"), ("Mrs. White", "p"), ("Kitchen", "r")]

class Card:
    def __init__(self, name, catagory):
        self.name = name
        self.catagory = catagory

    def __str__(self):
        return self.name

    @classmethod
    def build_deck(cls):
        deck = [];
        for cards, catagory in clueCards:
            deck.append(Card(cards, catagory))

        print [str(x) for x in deck]  # DEBUG
        return deck



Card.build_deck()
