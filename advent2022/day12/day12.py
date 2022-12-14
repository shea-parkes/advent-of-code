"""Crazy maze runner"""
import string
import typing

import cytoolz.curried as z
import cytoolz.curried.operator as zop

with open("input.txt", encoding="utf-8") as fh_in:
    raw = fh_in.read()

map_letters = {}
for idx_row, row in enumerate(raw.strip().split()):
    for idx_col, letter in enumerate(row):
        map_letters[idx_col, idx_row] = letter

get_unique_coord = lambda letter: z.pipe(
    map_letters,
    z.valfilter(zop.eq(letter)),
    dict.keys,
    z.first,
)
coord_start = get_unique_coord("S")
coord_end = get_unique_coord("E")

letter_values = {letter: idx for idx, letter in enumerate(string.ascii_lowercase)}
letter_values["S"] = 0
letter_values["E"] = 25

map_values = {coord: letter_values[letter] for coord, letter in map_letters.items()}


def path_finder(
    start: typing.Tuple[int, int],
    terminal_check: typing.Callable[[typing.Tuple[int, int]], bool],
    jump_fail_check: typing.Callable[[int, int], bool],
) -> typing.Mapping[typing.Tuple[int, int], int]:
    """Find the shortest path to the end"""
    min_travel: typing.Mapping[typing.Tuple[int, int], int] = {
        start: 0,
    }

    def recurse_fun(
        coord: typing.Tuple[int, int],
        height: int,  # Accept height as a parameter just to avoid another dict lookup
        cumm_distance: int,
        distances: typing.Mapping[typing.Tuple[int, int], int],
    ) -> None:
        """Recursive fun to solve"""

        if terminal_check(coord):
            # Do terminal check, but may not actually be shortest
            return None
        x_coord, y_coord = coord
        potentials = (
            (x_coord + 1, y_coord),
            (x_coord, y_coord + 1),
            (x_coord, y_coord - 1),
            (x_coord - 1, y_coord),
        )
        next_distance = cumm_distance + 1
        for potential in potentials:
            try:
                potential_height = map_values[potential]
            except KeyError:
                # Not on the map
                continue
            if jump_fail_check(height, potential_height):
                # Can't jump that high
                continue
            try:
                if next_distance >= distances[potential]:
                    # We've already gotten there in an equivalent-or-better time
                    continue
            except KeyError:
                # We haven't been here yet
                pass
            # Alright, let's move
            distances[potential] = next_distance
            recurse_fun(potential, potential_height, next_distance, distances)
        return None

    # Actually do the walking
    recurse_fun(start, map_values[start], 0, min_travel)
    return min_travel


print(
    path_finder(
        start=coord_start,
        terminal_check=zop.eq(coord_end),
        jump_fail_check=lambda old, new: (old + 1) < new,
    )[coord_end]
)

check_if_floor = z.compose_left(
    map_values.get,
    zop.eq(0),
)

all_backwards = path_finder(
    start=coord_end,
    terminal_check=check_if_floor,
    jump_fail_check=lambda old, new: (old - 1) > new,
)

z.pipe(
    all_backwards,
    z.keyfilter(check_if_floor),
    dict.values,
    z.topk(1, key=zop.neg),
    print,
)
