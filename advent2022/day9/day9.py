import itertools
import typing

import numpy as np

with open("input.txt") as fh_in:
    raw = fh_in.read().strip()


class PositionOnGrid(typing.NamedTuple):
    """A class representing a position on a grid"""

    x: int = 0
    y: int = 0


class ThingOnGrid:
    """A generic thing that can be on a grid"""

    def __init__(self):
        """Slap some initial state"""
        self.pos = PositionOnGrid()

    def U(self):
        """Move up"""
        self.pos = PositionOnGrid(self.pos.x, self.pos.y + 1)

    def D(self):
        """Move down"""
        self.pos = PositionOnGrid(self.pos.x, self.pos.y - 1)

    def L(self):
        """Move left"""
        self.pos = PositionOnGrid(self.pos.x - 1, self.pos.y)

    def R(self):
        """Move right"""
        self.pos = PositionOnGrid(self.pos.x + 1, self.pos.y)

    def is_adjacent(self, other) -> bool:
        """Check adjacency"""
        if abs(self.pos.x - other.pos.x) > 1:
            return False
        return abs(self.pos.y - other.pos.y) <= 1

    def snuggle_up(self, other) -> None:
        """Snuggle up to another position"""
        if self.is_adjacent(other):
            return None
        self.pos = PositionOnGrid(
            x=self.pos.x + np.sign(other.pos.x - self.pos.x),
            y=self.pos.y + np.sign(other.pos.y - self.pos.y),
        )


head = ThingOnGrid()
tail = ThingOnGrid()
visited_positions = set([tail.pos])
for move in raw.split("\n"):
    assert tail.is_adjacent(head)
    direction, distance = move.split()
    # print(f"Moving {distance} in {direction}")
    mover = getattr(head, direction)
    for _ in range(int(distance)):
        mover()
        tail.snuggle_up(head)
        # print(f"Head {head.pos.x},{head.pos.y} Tail {tail.pos.x},{tail.pos.y}")
        assert tail.is_adjacent(head)
        visited_positions.add(tail.pos)
print(len(visited_positions))


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


knots = [ThingOnGrid() for _ in range(10)]
visited_positions = set([PositionOnGrid()])
for move in raw.split("\n"):
    assert tail.is_adjacent(head)
    direction, distance = move.split()
    # print(f"Moving {distance} in {direction}")
    mover = getattr(knots[0], direction)
    for _ in range(int(distance)):
        mover()
        for lead, follow in pairwise(knots):
            follow.snuggle_up(lead)
            assert follow.is_adjacent(lead)
        visited_positions.add(knots[-1].pos)
print(len(visited_positions))
