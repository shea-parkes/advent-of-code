"""CY2022 Day10"""

with open("input.txt", encoding="utf-8") as fh_in:
    raw = fh_in.read()

cycles = []
current = 1
for instruction in raw.strip().split("\n"):
    if instruction == "noop":
        cycles.append(current)
        continue
    adjustment = int(instruction.split()[1])
    cycles.extend([current] * 2)
    current += adjustment

checks = (20, 60, 100, 140, 180, 220)
total = 0
for check in checks:
    value = cycles[check - 1]
    total += value * check
print(total)

marks = []
for crt, cycle in enumerate(cycles):
    crt_mod = crt % 40
    if not crt_mod:
        marks.append("\n")
    if abs(crt_mod - cycle) <= 1:
        marks.append("#")
    else:
        marks.append(".")

with open("output.txt", mode="w", encoding="utf-8") as fh_out:
    fh_out.write("".join(marks))
