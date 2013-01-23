# I removed the big tag up top for now. Feel free to add it if you like
# Also removed the '#!/bin/python' bit as this script will never be run

# The namedtuple will be used for handling locations
from collections import namedtuple

# I moved the grid to a separate file because it cluttered up this one.
# Might as well keep the ugly contained, ya know?
from grid import grid


# This essentially creates a non-mutable class.
# You can create locations using the normal instantiation notation:
# a_location = Location(4, 2)
# some_location = Location(x=10, y=23)
# another_location = Location(y=23, x=10)

# Rather than passing an 'x' and 'y' argument to each method and worrying
# about their order, let's just abstract the concept into a location object
# and just pass that! Notice how much nicer the API is for each of the
# methods in the 'Board' class.
Location = namedtuple('Location', ['x', 'y'])

# This is essentially an enum. We use destructuring (tuple unpacking)
# to assign the numbers 0 through 3 to the given names. The only reason
# we do this is to increase readability. I'd rather see INACCESSABLE
# than a simple zero int.
INACCESSABLE, NORMAL, DOOR_EW, DOOR_NS = range(4)


# This is currently only used in one case where a method is called to
# determine if a door is accessable and the given destination is not
# a door. I'd rather be notified if that method is being called when
# it shouldn't than simply being given a False result. Sometimes, breaking
# is a better behavior than tenacity, particularly when building up the
# program
class NotCorrectTileError(Exception):
    """Used to indicate that a tile is not the type of tile expected"""


# I renamed this to 'Board' from 'GameBoard' because I felt that the
# previous name didn't add anything by prepending 'Game' to the name.
class Board(object):
    # Docstrings are good. Use them so that you understand what things
    # are supposed to do. Don't spend time on implementation details,
    # just talk about the general idea of the method or class.
    """The board on which the Sleuth game is played

    The Board is a singleton with only class methods and attributes. This
    class is used in making determiniations and no method will mutate any
    given argument or state of the Board.
    """
    # This 'private' dict will translate the grid numbers to the
    # enums created above.
    _tile_type = {0: INACCESSABLE,
                  1: NORMAL,
                  2: DOOR_EW,
                  3: DOOR_NS}

    # Much cleaner than having the actual large grid here!
    _grid = grid

    # Since this is a singleton, we'll cache the only instance here.
    # More on this shortly (__new__)
    _board_instance = None

    # The __new__ method is used when creating a class. This is a class
    # method rather than an instance method. As such, we use 'cls' (by
    # convention) rather than 'self'. You'll be seeing this a lot in the
    # other methods in this class. Instead of an instance being passed
    # (no instance exists at this point!), the actual 'Board' class is
    # passed (this is true in all class methods). We first check to see
    # if an instance of the Board exists at Board._board_instance and
    # if there is not, we create one and assign it to that class variable.
    # Once we're sure that an instance does exist (whether we created one
    # or if one already existed), we return that instance.
    def __new__(cls, *args, **kwargs):
        if not cls._board_instance:
            # Python 2 syntax for 'super' sucks. That's life.
            cls._board_instance = super(Board, cls).__new__(
                cls, *args, **kwargs)

        return cls._board_instance

    # Only the __new__ method is implicitly a class method, all others
    # must be declared as such. We do so using this decorator.
    # This decorator is the same as using: classmethod(board_width)
    # A class method belongs to the class, and when called (even from
    # an instance, the class of that instance ('Board' in this case) is
    # passed instead of the usual instance. For that reason, it is convention
    # to use 'cls' as the first parameter instead of 'self'.
    @classmethod
    # Another decorator! This time, we're asking the method to behave as
    # if it were an attribute (member variable) of the class:
    # Board.board_width rather than Board.board_width()
    # This is a stylistic choice, and I do so because there are no args
    # to be passed and so it seems a good candidate to become a
    # virtual attribute.
    def board_width(cls):
        """Width of the game board in tiles"""
        return len(cls._grid[0])

    # Same thing as above, but this time for height.
    @classmethod
    def board_height(cls):
        """Height of the game board in tiles"""
        return len(cls._grid)

    @classmethod
    # Isn't that function signature nicer than "tile_at(cls, x, y)"?
    # This is just part of why the Location namedtuple is a good idea.
    def tile_at(cls, location):
        """Determine the type of tile at a given location on the board."""
        # I could have used the following:
        # return cls._tile_type[cls._grid[location.y][location.x]]
        # but that's long, complicated, and hard to understand quickly.

        # Essentially we're performing the following atomic actions:
        # row = cls._grid[location.y]
        # cell = row[location.x]
        # tile = cls._tile_type[cell]
        # return tile

        # I like to break this down somewhat for the sake of readability,
        # even if it makes it slightly less terse. Readability is king!

        # Readability is also improved due to the Location namedtuple.
        # Instead of dealing with indexing a tuple, we have an object
        # with attributes (Namedtuples can be indexed too!).
        tile = cls._grid[location.y][location.x]
        return cls._tile_type[tile]

    # You already had something like this in your 'move' method, but
    # remember how readability is king? I like to have actions like this
    # be named so that when used in the context of some other more complex
    # method, it's immediately obvious what's going on rather than having
    # to parse the code. Names are good and support readability!
    @classmethod
    def is_accessable(cls, location):
        """Determines if a tile is an accessable tile"""
        return cls.tile_at(location) is not INACCESSABLE

    # Again, this was in the 'move' method, but it was factored into
    # its own method to name the action and improve readability.
    @classmethod
    def in_board(cls, location):
        """Determines if a location is inside of the board dimensions"""
        # I find the following more readable than breaking it into
        # two conditions like this:
        # 0 <= location.x and location.x < cls.board_width
        # They're the same, but I find it to be cleaner syntax. Up to you.
        return (0 <= location.x < cls.board_width() and
                0 <= location.y < cls.board_height())

    # This was the more complex part of the 'move' method, and it was not
    # immediately apparent what was going on in the code. After spending a
    # few seconds reading the method, you can understand, but why not name
    # the action and make it more easily understandable?
    @classmethod
    def door_accessable(cls, location, door_location):
        """Determine if a door is accessable from given location

        If a door is of the North/South variety, it is accessable only from
        the tile above or below it. If the given door location is East/West,
        it is accessable only from the tile to the left or to the right.

        Raises a NotCorrectTileError if the given door location is not a door.
        """
        tile_type = cls.tile_at(door_location)

        if not cls.is_door(door_location):
            raise NotCorrectTileError("Given tile ({}, {}) not a door".format(
                door_location.x, door_location.y))

        if tile_type is DOOR_NS:
            # Given my earlier comments about naming actions, one might
            # be tempted to make a method: Board.same_row and
            # Board.same_column, but I feel that this is a simple and
            # obvious enough action to leave unnamed. There's a line to be
            # drawn between readability and overly verbose and it's up to
            # you to define it.
            return (location.x == door_location.x and
                    location.y == door_location.y + 1 or
                    location.y == door_location.y - 1)
        elif tile_type is DOOR_EW:
            return (location.y == door_location.y and
                    location.x == door_location.x + 1 or
                    location.x == door_location.x - 1)
        else:
            return False

    # This is an example of some code that I feel is obvious enough to
    # not need a name, but it is used in two places in various methods,
    # so let's pull it into a method so that we don't need to repeat
    # ourselves. This is known as the DRY principle (Don't Repeat Yourself).
    # When we repeat ourselves, we have to be concerned with changing code
    # in multiple locations, which can lead to bugs if we modify one bit
    # and not the other. Beware of cutting and pasting code, or repeating code
    @classmethod
    def is_door(cls, location):
        """Determine if a given location is a door"""
        return cls.tile_at(location) in (DOOR_EW, DOOR_NS)

    # This was your 'move' method. Since 'move' is a verb, you might expect
    # such a method to mutate one of the arguments, or some state. Since
    # this does not, nor does it do any actual moving, I feel that this
    # (or some similar phrase) is a better name. This was a fairly
    # difficult method to parse before. Check the difference between the
    # readability of the 'move' method before the refactoring and now.
    # Notice how the named actions that have been refactored into methods
    # help a reader to immediately understand what the code is trying to do?
    @classmethod
    def available_destinations(cls, roll, start_location, exclude):
        """Determine the places to which a player may move

        Given a Location from which to start and a roll representing the
        times a player may traverse tiles, determines the legal destinations
        and returns them in a set recursively.

        Locations in the exclude set will be excluded from the legal
        destinations.
        """
        if roll == 0:
            # We use set methods union and update later, which expect sets
            # and this was a list. Make sure to read the docs and/or test
            # your ideas in an interpreter to make sure that you're using
            # methods the right way. Understanding methods is important in
            # a non-explicitly typed language like Python. Instead of a
            # compiler or IDE warning, you'll just get an TypeError. Try
            # it in your interpreter.
            return {start_location}

        legal_moves = set()
        for location in cls.adjacent_locations(start_location):
            #if location.x == 9 and location.y == 7:
                #import ipdb; ipdb.set_trace()

            if location in exclude:
                continue

            if not cls.in_board(location) or not cls.is_accessable(location):
                continue

            if (cls.is_door(location) and
                    not cls.door_accessable(start_location, location)):
                continue

            # I broke these steps down to reduce apparent complexity to
            # a reader. I could have chained the methods together and all,
            # but it would have been slightly more difficult to read, and
            # an extra line is a small price to pay for readability!
	    #
	    # Added condition for if the location is good, and is a door
            if cls.is_door(location):
                destinations = {location}
            else:
                destinations = cls.available_destinations(
                    roll - 1, location, exclude.union({start_location}))
            # Notice the use of 'union' above and set method 'update' below?
            # The two methods do similar tasks (join sets, essentially), but
            # 'union' produces a new set object while 'update' mutates the
            # set instance that calls it. It's important to read the docs
            # and understand the methods and what they do.

            # Also, you tried to concatenate a set with a list in your method,
            # which won't work. I chose to use the set.union method instead
            # of mutating the set object else each recursion would be working
            # off of the same set object, which we don't necessarily want.
            # Or maybe we do, that one you'll have to let me know about.
            legal_moves.update(destinations)

        # Your scoping of legal_moves (or whatever it was called before)
        # was such that it was contained in the for-loop which would cause
        # the method to return before iterating through each of the possible
        # adjacent locations.
        return legal_moves

    @classmethod
    def adjacent_locations(cls, location):
        """Returns a list of locations adjacent to a given location

        Adjacency is defined as those locations above, below, to the left,
        or to the right of a given location
        """
        # We have a Location namedtuple, so we'll be sure to use it.
        # Try not to deal in raw data like an 'x' and 'y' int or even a
        # tuple if you don't have to. Names are good and I'd rather ask
        # for an attribute than index a tuple:
        # location_namedtuple.x vs location_tuple[0]
        # It may be a good choice to name the arguments, up to you.
        # ie. Location(x=location.x - 1, y=location.y)
        return [Location(location.x - 1, location.y),
                Location(location.x + 1, location.y),
                Location(location.x, location.y - 1),
                Location(location.x, location.y + 1)]
