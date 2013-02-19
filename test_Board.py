import pytest

from board import (Board, Location, NotCorrectTileError,
                   ShouldNotBeInstantiated, INACCESSABLE, NORMAL, DOOR_EW,
                   DOOR_NS, IncompatibleInterfaceException)

@pytest.mark.parametrize(('inpt', 'expected'), [
    (0, INACCESSABLE),
    (1, NORMAL),
    (2, DOOR_EW),
    (3, DOOR_NS),
])
def test_tile_type(inpt, expected):
    assert Board._tile_type[inpt] == expected

def test_instantiation():
    with pytest.raises(ShouldNotBeInstantiated):
        board = Board()

@pytest.mark.parametrize(('inpt', 'expected'), [
    (Location(0, 0), INACCESSABLE),
    (Location(7, 8), NORMAL),
    (Location(5, 7), NORMAL),
    (Location(14, 12), INACCESSABLE),
    (Location(7, 12), DOOR_EW),
    (Location(22, 12), DOOR_NS),
    (Location(10, 23), INACCESSABLE),
    (Location(18, 19), NORMAL),
])
def test_tile_at(inpt, expected):
    assert Board.tile_at(inpt) == expected

@pytest.mark.parametrize(('inpt', 'expected'), [
    (Location(0, 0), False),
    (Location(7, 8), True),
    (Location(5, 7), True),
    (Location(14, 12), False),
    (Location(7, 12), True),
    (Location(22, 12), True),
    (Location(10, 23), False),
    (Location(18, 19), True),
])
def test_is_accessable(inpt, expected):
    assert Board.is_accessable(inpt) == expected

@pytest.mark.parametrize(('inpt', 'expected'), [
    (Location(0, 0), True),
    (Location(50, 29), False),
    (Location(7, 8), True),
    (Location(9999999, 1), False),
    (Location(5, 7), True),
    (Location(-10, 5), False),
    ({1: 23, 9: 76, 'a': 'b'}, None),
    (Location(14, 12), True),
    (Location(7, 12), True),
    (Location(22, 12), True),
    (("ten", "five"), None),
    (Location(10, 23), True),
    ((7, 5), None),
    (Location(18, 19), True),
])
def test_in_board(inpt, expected):
    def assertion():
        assert Board.in_board(inpt) == expected

    if expected is None:
        with pytest.raises(IncompatibleInterfaceException):
            assertion()
    else:
        assertion()


#@pytest.mark.parametrize(('loc', 'doorloc', 'expected'), [
#    (Location(7, 4), Location(7,5), True),
#    (Location(8, 5), Location(7,5), True),
#   (Location(7, 6), Location(7,5), True),
#    (Location(6, 5), Location(7,5), True),
#    ])
#def test_door_Accessable(loc, doorloc, expected):
#    assert Board.is_accessable(loc, doorloc) == expected










