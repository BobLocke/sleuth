
# The namedtuple will be used for handling locations
from collections import namedtuple
from grid import grid


Location = namedtuple('Location', ['x', 'y'])

INACCESSABLE, NORMAL, DOOR_EW, DOOR_NS = range(4)


class NotCorrectTileError(Exception):
    """Used to indicate that a tile is not the type of tile expected."""


class ShouldNotBeInstantiated(Exception):
    """Error that occurs when attempting to instantiate"""


class IncompatibleInterfaceException(Exception):
    """Error occurs when receiving an unexpected object"""


class Board(object):
    """The board on which the Sleuth game is played

    The Board is a singleton with only class methods and attributes. This
    class is used in making determiniations and no method will mutate any
    given argument or state of the Board.
    """

    _tile_type = {0: INACCESSABLE,
                  1: NORMAL,
                  2: DOOR_EW,
                  3: DOOR_NS}

    _grid = grid

    def __new__(cls, *args, **kwargs):
        raise ShouldNotBeInstantiated("Board should not be instantiated")

    @classmethod
    def tile_at(cls, location):
        """Determine the type of tile at a given location on the board."""
        try:
            tile = cls._grid[location.y][location.x]
            return cls._tile_type[tile]
        except AttributeError:
            raise IncompatibleInterfaceException("Expected an object with "
                                                 "'x', and 'y' attributes")

    @classmethod
    def is_accessable(cls, location):
        """Determines if a tile is an accessable tile"""
        return cls.tile_at(location) is not INACCESSABLE

    @classmethod
    def in_board(cls, location):
        """Determines if a location is inside of the board dimensions"""
        try:
            return (0 <= location.x < len(cls._grid[0]) and
                    0 <= location.y < len(cls._grid))
        except AttributeError:
            raise IncompatibleInterfaceException("Expected an object with "
                                                 "'x', and 'y' attributes")

    @classmethod
    def door_accessable(cls, location, door_location):
        """Determine if a door is accessable from given location

        If a door is of the North/South variety, it is accessable only from
        the tile above or below it. If the given door location is East/West,
        it is accessable only from the tile to the left or to the right.

        Raises a NotCorrectTileError if the given door location is not a door.
        """
        tile_type = cls.tile_at(door_location)

        try:
            if not cls.is_door(door_location):
                raise NotCorrectTileError("Given tile ({}, {}) not a door".format(
                    door_location.x, door_location.y))

            if tile_type is DOOR_NS:
                return (location.x == door_location.x and
                        location.y == door_location.y + 1 or
                        location.y == door_location.y - 1)
            elif tile_type is DOOR_EW:
                return (location.y == door_location.y and
                        location.x == door_location.x + 1 or
                        location.x == door_location.x - 1)
            else:
                return False
        except AttributeError:
            raise IncompatibleInterfaceException("Expected an object with "
                                                 "'x', and 'y' attributes")
    @classmethod
    def is_door(cls, location):
        """Determine if a given location is a door"""
        return cls.tile_at(location) in (DOOR_EW, DOOR_NS)

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
            return {start_location}

        legal_moves = set()
        for location in cls.adjacent_locations(start_location):

            if location in exclude:
                continue

            if not cls.in_board(location) or not cls.is_accessable(location):
                continue

            if (cls.is_door(location) and
                    not cls.door_accessable(start_location, location)):
                continue

            if cls.is_door(location):
                destinations = {location}
            else:
                destinations = cls.available_destinations(
                    roll - 1, location, exclude.union({start_location}))

            #Bob:
            # I'm not sure, I'd think we want only the one object returned.
            # I don't think mutating the original really hurts anything?
            # All we're doing is adding to it, and duplicates get pruned
            # by it being a set. I'll ask about this when we meet.
            # What's here works, but it might be less efficent.

            legal_moves.update(destinations)
        return legal_moves

    @classmethod
    def adjacent_locations(cls, location):
        """Returns a list of locations adjacent to a given location

        Adjacency is defined as those locations above, below, to the left,
        or to the right of a given location"""

        try:
            return [Location(location.x - 1, location.y),
                    Location(location.x + 1, location.y),
                    Location(location.x, location.y - 1),
                    Location(location.x, location.y + 1)]
        except AttributeError:
            raise IncompatibleInterfaceException("Expected an object with "
                                                 "'x', and 'y' attributes")
