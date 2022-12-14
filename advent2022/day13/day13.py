"""Day 13 of CY2022 fun"""
import functools
import itertools
import typing

import cytoolz.curried as z
import cytoolz.curried.operator as zop

with open("input.txt", encoding="utf-8") as fh_in:
    raw = fh_in.read()


def grouper(iterable, n=2):
    """Give things two at a time"""
    list_of_iters = [iter(iterable)] * n
    return zip(*list_of_iters)


clean_pairs = z.pipe(
    raw.rstrip().replace("\n\n", "\n").split(),
    z.map(eval),
    grouper,
    tuple,
)


def compare(
    left: typing.Union[int, list],
    right: typing.Union[int, list],
) -> typing.Optional[bool]:
    """Basic unit of comparison"""
    # print(f"Comparing {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])

    for ileft, iright in itertools.zip_longest(left, right):
        if ileft is None:
            return True
        if iright is None:
            return False
        icompare = compare(ileft, iright)
        if icompare is not None:
            return icompare


assert compare([[1], [2, 3, 4]], [[1], 4])
assert not compare(
    [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
    [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
)

total = 0
for index, pair in enumerate(clean_pairs):
    if compare(*pair):
        total += index + 1
print(total)


def compare_for_sort(left, right) -> int:
    """Make it happy for Python sort API"""
    return -1 if compare(left, right) else 1


ordered = z.pipe(
    raw.rstrip().replace("\n\n", "\n").split(),
    z.map(eval),
    list,
    zop.add([[[2]]]),
    zop.add([[[6]]]),
    z.partial(
        sorted,
        key=functools.cmp_to_key(compare_for_sort),
    ),
)

get_ordered_index = z.compose_left(
    zop.indexOf(ordered),
    zop.add(1),
)

print(
    zop.mul(
        get_ordered_index([[2]]),
        get_ordered_index([[6]]),
    )
)
