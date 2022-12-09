with open("input.txt") as fh_in:
    raw = fh_in.read()

clean = [tuple(x.split()) for x in raw.strip().split("\n")]


my_choice = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}
my_score = sum(my_choice[game[1]] for game in clean)

compete = {
    ("A", "X"): 3,
    ("A", "Y"): 6,
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("B", "Y"): 3,
    ("B", "Z"): 6,
    ("C", "X"): 6,
    ("C", "Y"): 0,
    ("C", "Z"): 3,
}
compete_score = sum(compete[game] for game in clean)

swap = {
    ("A", "X"): "C",
    ("A", "Y"): "A",
    ("A", "Z"): "B",
    ("B", "X"): "A",
    ("B", "Y"): "B",
    ("B", "Z"): "C",
    ("C", "X"): "B",
    ("C", "Y"): "C",
    ("C", "Z"): "A",
}
decoded = [(game[0], swap[game]) for game in clean]

my_choice = {
    "A": 1,
    "B": 2,
    "C": 3,
}
compete = {
    ("A", "A"): 3,
    ("A", "B"): 6,
    ("A", "C"): 0,
    ("B", "A"): 0,
    ("B", "B"): 3,
    ("B", "C"): 6,
    ("C", "A"): 6,
    ("C", "B"): 0,
    ("C", "C"): 3,
}
my_score = sum(my_choice[game[1]] for game in decoded)
compete_score = sum(compete[game] for game in decoded)
