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
class FancyRange:
    """Fancy range thing"""

    start: int
    stop: int

    def combine(self, other):
        """Try combining"""
        if (self.stop + 1) == other.start:
            return FancyRange(self.start, other.stop)
        if (other.stop + 1) == self.start:
            return FancyRange(other.start, self.stop)
        if self.stop < other.start:
            return None
        if other.stop < self.start:
            return None
        return FancyRange(min(self.start, other.start), max(self.stop, other.stop))

    def __len__(self):
        """Standard len fun"""
        return self.stop - self.start + 1


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
        # print(f"I am {self}.  My min_x_impossible is {min_x_impossible}")
        assert not self.position_possible(min_x_impossible, other_y)
        assert self.position_possible(min_x_impossible - 1, other_y)
        max_x_impossible = self.sensor_x + dist_for_x - 1
        # print(f"I am {self}.  My max_x_impossible is {max_x_impossible}")
        assert not self.position_possible(max_x_impossible, other_y)
        assert self.position_possible(max_x_impossible + 1, other_y)
        return FancyRange(min_x_impossible, max_x_impossible)


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


@z.curry
def get_impossibles(y_, sensors, *, min_x=None, max_x=None):
    """Get the impossibles"""
    fancy_ranges = []
    for sensor in sensors:
        # print(f"Fancy ranges is now {fancy_ranges}")
        new_range = sensor.set_x_impossible(y_)
        if new_range is None:
            continue
        if min_x and min_x > new_range.stop:
            continue
        if max_x and max_x < new_range.start:
            continue
        # print(f"New range is {new_range}")
        if not fancy_ranges:
            fancy_ranges.append(new_range)
            continue
        overlaps = []
        for index, fancy_range in enumerate(fancy_ranges):
            if new_range.combine(fancy_range) is not None:
                overlaps.append(index)
        if not overlaps:
            fancy_ranges.append(new_range)
            continue
        for index in overlaps:
            new_range = new_range.combine(fancy_ranges[index])
        fancy_ranges = [x for i, x in enumerate(fancy_ranges) if i not in overlaps]
        fancy_ranges.append(new_range)
    return fancy_ranges


BEACON_ON_ROW = {sensor.beacon_x for sensor in SENSORS if sensor.beacon_y == 2_000_000}

z.pipe(
    SENSORS,
    get_impossibles(2_000_000),
    z.map(len),
    sum,
    z.flip(zop.sub)(len(BEACON_ON_ROW)),
)


for poss_y in range(0, 4_000_000 + 1):
    if not poss_y % 40_000:
        print(f"Checking {poss_y}")
    imposs_x = get_impossibles(poss_y, SENSORS, min_x=0, max_x=4_000_000)
    if len(imposs_x) > 1:
        print(f"Poss_y is {poss_y} and imposs_x is {imposs_x}")
        break

# Poss_y is 2628223 and imposs_x is [FancyRange(start=2939044, stop=4145968), FancyRange(start=-1333240, stop=2939042)]

print(2_939_043 * 4_000_000 + 2_628_223)
