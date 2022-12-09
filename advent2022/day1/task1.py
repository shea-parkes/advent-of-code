with open("input.txt") as fh_in:
    raw = fh_in.read()

clean = [list(map(int, x.split())) for x in raw.rstrip().split("\n\n")]
elfs = list(map(sum, clean))
max(elfs)
sum(sorted(elfs)[-3:])
