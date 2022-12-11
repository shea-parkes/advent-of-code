"""Day 11, CY2022.  Monkey flinging"""
import collections
import dataclasses
import operator as op
import typing

import cytoolz.curried as z


def is_divisible(denom):
    """Build a divisibility checker"""
    return z.compose_left(
        z.flip(op.mod)(denom),
        op.not_,
    )


@dataclasses.dataclass
class Monkey:
    """Silly class"""

    items: collections.deque
    operation: typing.Callable[[int], int]
    test: typing.Callable[[int], bool]
    target_true: int
    target_false: int
    throw_count: int = 0

    def throw_item(self, monkeys):
        """Throw an item"""
        self.throw_count += 1
        item = self.items.popleft()
        item = self.operation(item)
        # item = item // 3
        item = item % (19 * 13 * 5 * 7 * 17 * 2 * 3 * 11)
        target = self.target_true if self.test(item) else self.target_false
        monkeys[target].items.append(item)

    def throw_all_items(self, monkeys):
        """Throw all the damn items"""
        for _ in range(len(self.items)):
            self.throw_item(monkeys)


MONKEYS = (
    Monkey(
        items=collections.deque((93, 98)),
        operation=z.curry(op.mul)(17),
        test=is_divisible(19),
        target_true=5,
        target_false=3,
    ),
    Monkey(
        items=collections.deque((95, 72, 98, 82, 86)),
        operation=z.curry(op.add)(5),
        test=is_divisible(13),
        target_true=7,
        target_false=6,
    ),
    Monkey(
        items=collections.deque((85, 62, 82, 86, 70, 65, 83, 76)),
        operation=z.curry(op.add)(8),
        test=is_divisible(5),
        target_true=3,
        target_false=0,
    ),
    Monkey(
        items=collections.deque((86, 70, 71, 56)),
        operation=z.curry(op.add)(1),
        test=is_divisible(7),
        target_true=4,
        target_false=5,
    ),
    Monkey(
        items=collections.deque((77, 71, 86, 52, 81, 67)),
        operation=z.curry(op.add)(4),
        test=is_divisible(17),
        target_true=1,
        target_false=6,
    ),
    Monkey(
        items=collections.deque((89, 87, 60, 78, 54, 77, 98)),
        operation=z.curry(op.mul)(7),
        test=is_divisible(2),
        target_true=1,
        target_false=4,
    ),
    Monkey(
        items=collections.deque((69, 65, 63)),
        operation=z.curry(op.add)(6),
        test=is_divisible(3),
        target_true=7,
        target_false=2,
    ),
    Monkey(
        items=collections.deque((89,)),
        operation=z.flip(op.pow)(2),
        test=is_divisible(11),
        target_true=0,
        target_false=2,
    ),
)

for _ in range(10_000):
    for monkey in MONKEYS:
        monkey.throw_all_items(MONKEYS)

z.pipe(
    MONKEYS,
    z.map(z.flip(getattr)("throw_count")),
    z.topk(2),
    z.reduce(op.mul),
)
