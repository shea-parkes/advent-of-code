"""Day 15 of the CY2022 Advent of code"""
import dataclasses
import itertools
import re

import cytoolz.curried as z
import cytoolz.curried.operator as zop

with open("input.txt", encoding="utf-8") as fh_in:
    raw = fh_in.read()

PATTERN = re.compile(
    r"Sensor at x=(?P<sensor_x>[-\d]+), y=(?P<sensor_y>[-\d]+): closest beacon is at x=(?P<beacon_x>[-\d]+), y=(?P<beacon_y>[-\d]+)"
)


def calc_dist(alpha, beta):
    """Simple distance fun"""
    return abs(alpha[0] - beta[0]) + abs(alpha[1] - beta[1])


@dataclasses.dataclass
class Sensor:
    """Quick and dirty sensor"""

    sensor_x: int
    sensor_y: int
    beacon_x: int
    beacon_y: int
    _dist_to_beacon: int = dataclasses.field(init=False)

    def __post_init__(self):
        self._dist_to_beacon = self.dist_to_other(self.beacon_x, self.beacon_y)

    def dist_to_other(self, other_x, other_y):
        """Distance to something else"""
        return abs(self.sensor_x - other_x) + abs(self.sensor_y - other_y)

    def position_possible(self, other_x, other_y):
        """Is it possible there is a beacon there"""
        return self._dist_to_beacon < self.dist_to_other(other_x, other_y)

    def any_x_possible(self, other_y):
        """Is there any possible touch"""
        dist_for_x = self._dist_to_beacon - abs(self.sensor_y - other_y) + 1
        return dist_for_x > 0

    def set_x_impossible(self, other_y):
        """Set of all impossible x for a given y"""
        dist_for_x = self._dist_to_beacon - abs(self.sensor_y - other_y) + 1
        if dist_for_x <= 0:
            return None
        min_x_impossible = self.sensor_x - dist_for_x + 1
        print(f"I am {self}.  My min_x_impossible is {min_x_impossible}")
        assert not self.position_possible(min_x_impossible, other_y)
        assert self.position_possible(min_x_impossible - 1, other_y)
        max_x_impossible = self.sensor_x + dist_for_x - 1
        print(f"I am {self}.  My max_x_impossible is {max_x_impossible}")
        assert not self.position_possible(max_x_impossible, other_y)
        assert self.position_possible(max_x_impossible + 1, other_y)
        return set(range(min_x_impossible, max_x_impossible + 1))


SENSORS = z.pipe(
    raw.rstrip().split("\n"),
    z.map(
        z.compose_left(
            z.curry(re.search)(PATTERN),
            lambda x: Sensor(
                int(x.group("sensor_x")),
                int(x.group("sensor_y")),
                int(x.group("beacon_x")),
                int(x.group("beacon_y")),
            ),
        ),
    ),
    tuple,
)

BEACON_ON_ROW = {sensor.beacon_x for sensor in SENSORS if sensor.beacon_y == 2_000_000}

z.pipe(
    SENSORS,
    z.map(z.flip(Sensor.set_x_impossible, 2_000_000)),
    z.curry(itertools.filterfalse)(zop.is_(None)),
    z.reduce(zop.or_),
    z.flip(zop.sub)(BEACON_ON_ROW),
    len,
)
