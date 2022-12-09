with open("input.txt") as fh_in:
    raw = fh_in.read().strip().split("\n")

clean = []
for row in raw:
    messy_list = []
    elves = row.split(",")
    for elf in elves:
        messy_list.extend(elf.split("-"))
    clean.append(tuple(int(x) for x in messy_list))

print(clean)


expanded = [(set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))) for x in clean]

sum(not (x - y) or not (y - x) for x, y in expanded)

sum(bool(x & y) for x, y in expanded)
