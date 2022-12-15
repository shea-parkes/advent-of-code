"""Day 14 CY2022"""
import itertools

import cytoolz.curried as z
import cytoolz.curried.operator as zop
import numpy as np

with open("input.txt", encoding="utf-8") as fh_in:
    raw = fh_in.read()

zsplit = z.flip(str.split)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


paths = z.pipe(
    raw.rstrip(),
    zsplit("\n"),
    z.map(
        z.compose_left(
            zsplit(" -> "),
            z.map(
                z.compose_left(
                    zsplit(","),
                    z.map(int),
                    tuple,
                )
            ),
            tuple,
        )
    ),
    tuple,
)


@z.curry
def draw_line(state, beg, end):
    """Draw a line into the state"""
    state[beg] = "#"
    current = beg
    while current != end:
        # print(f"Current is {current}")
        current = (
            current[0] + np.sign(end[0] - current[0]),
            current[1] + np.sign(end[1] - current[1]),
        )
        state[current] = "#"
    return None


test_cave = {}
draw_line(test_cave, (0, 3), (5, 3))
assert len(test_cave) == 6

cave = {}
for path in paths:
    for beg, end in pairwise(path):
        draw_line(cave, beg, end)

cave_floor = z.pipe(
    cave,
    dict.keys,
    z.map(z.get(1)),
    max,
)


@z.curry
def fill_cave(check_dead, check_stopped, cave):
    """Fill a cave with sand"""
    cave_fill = cave.copy()
    sand_beg = (500, 0)
    done_filling = False
    while True:
        sand = sand_beg
        while True:
            # print(f"Sand falling at { sand }")
            if check_dead(sand):
                done_filling = True
                break
            if check_stopped(sand):
                break
            down = sand[0], sand[1] + 1
            if down not in cave_fill:
                sand = down
                continue
            down_left = sand[0] - 1, sand[1] + 1
            if down_left not in cave_fill:
                sand = down_left
                continue
            down_right = sand[0] + 1, sand[1] + 1
            if down_right not in cave_fill:
                sand = down_right
                continue
            break
        if done_filling:
            break
        # print(f"Adding sand at { sand }")
        cave_fill[sand] = "O"
        if sand_beg in cave_fill:
            break
    return cave_fill


def always(x):
    """Return a function that always returns this input"""

    def closure(*args, **kwargs):
        """Inner closure that ignores all of its args"""
        return x

    return closure


z.pipe(
    cave,
    fill_cave(
        z.compose_left(
            z.get(1),
            zop.lt(cave_floor),
        ),
        always(False),
    ),
    z.valfilter(zop.eq("O")),
    len,
    print,
)

z.pipe(
    cave,
    fill_cave(
        always(False),
        z.compose_left(
            z.get(1),
            zop.eq(cave_floor + 1),
        ),
    ),
    z.valfilter(zop.eq("O")),
    len,
    print,
)
