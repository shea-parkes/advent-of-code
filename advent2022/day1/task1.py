with open("input.txt") as fh_in:
    raw = fh_in.read()

clean = [list(map(int, x.split())) for x in raw.rstrip().split("\n\n")]
elfs = list(map(sum, clean))
max(elfs)
sum(sorted(elfs)[-3:])


import cytoolz.curried as z

elves = z.pipe(
    raw,
    str.rstrip,
    z.flip(str.split)("\n\n"),
    z.map(
        z.compose_left(
            str.split,
            z.map(int),
            sum,
        ),
    ),
    list,
)

max(elves)
z.pipe(
    elves,
    z.topk(3),
    sum,
)
