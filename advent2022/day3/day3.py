with open("input.txt") as fh_in:
    raw = fh_in.read()

clean = raw.strip().split()

import string

priority = {letter: index + 1 for index, letter in enumerate(string.ascii_letters)}


def get_priority(rucksack):
    """Get the priority of the mis-packed item"""
    split_point = len(rucksack) // 2
    left = rucksack[:split_point]
    right = rucksack[split_point:]
    assert len(left) == len(right)
    overlap = set(left) & set(right)
    assert len(overlap) == 1
    return priority[overlap.pop()]


total = 0
for rucksack in clean:
    total += get_priority(rucksack)
print(total)

sum(get_priority(bob) for bob in clean)
sum(map(get_priority, clean))


def grouper(iterable, n):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip(*args)


def get_group_priority(rucksacks):
    """Get priority of the set of rucksacks"""
    overlap = set(rucksacks[0]) & set(rucksacks[1]) & set(rucksacks[2])
    assert len(overlap) == 1
    return priority[overlap.pop()]


import functools


def get_group_priority(rucksacks):
    """Get priority of the set of rucksacks"""
    overlap = functools.reduce(
        set.intersection,
        map(set, rucksacks),
    )
    assert len(overlap) == 1
    return priority[overlap.pop()]


def get_group_priority(rucksacks):
    """Get priority of the set of rucksacks"""
    overlap = None
    for rucksack in rucksacks:
        if overlap is None:
            overlap = set(rucksack)
        else:
            overlap = overlap & set(rucksack)

    assert len(overlap) == 1
    return priority[overlap.pop()]


sum(get_group_priority(group) for group in grouper(clean, 3))
sum(map(get_group_priority, grouper(clean, 3)))
