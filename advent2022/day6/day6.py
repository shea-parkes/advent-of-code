with open("input.txt") as fh_in:
    raw = fh_in.read().strip()

import collections
import itertools


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def first_signal(stream, signal_size):
    for i, chunk in enumerate(sliding_window(stream, signal_size)):
        if len(chunk) == len(set(chunk)):
            return i + signal_size


print(first_signal("bvwbjplbgvbhsrlpgdmjqwftvncz", 4))
print(first_signal("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4))

print(first_signal(raw, 4))
print(first_signal(raw, 14))
