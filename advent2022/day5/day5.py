with open("moves.txt") as fh_in:
    moves_raw = fh_in.read()

moves_split = [x.split() for x in moves_raw.strip().split("\n")]
moves = [(int(x[1]), int(x[3]), int(x[5])) for x in moves_split]

with open("starts.txt") as fh_in:
    starts_raw = fh_in.read().rstrip().split("\n")


stacks = [[] for _ in range(9)]

for row in starts_raw[-2::-1]:
    for stack, column in enumerate(range(1, 34, 4)):
        value = row[column]
        if value == " ":
            continue
        stacks[stack].append(value)

print(stacks)

for move_n, move_from, move_to in moves:
    for _ in range(move_n):
        stacks[move_to - 1].append(stacks[move_from - 1].pop())

print(stacks)

print("".join(x[-1] for x in stacks))


stacks = [[] for _ in range(9)]

for row in starts_raw[-2::-1]:
    for stack, column in enumerate(range(1, 34, 4)):
        value = row[column]
        if value == " ":
            continue
        stacks[stack].append(value)

print(stacks)

for move_n, move_from, move_to in moves:
    load = []
    for _ in range(move_n):
        load.append(stacks[move_from - 1].pop())
    stacks[move_to - 1].extend(reversed(load))

print(stacks)

print("".join(x[-1] for x in stacks))
