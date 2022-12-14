with open("input.txt") as fh_in:
    raw = fh_in.read().rstrip().split("\n")


def parse_command_list(commands):
    """Build nested dictionaries. File values are their size."""
    root = {}
    cwd = root
    parents = []

    for line in commands:
        # print(f"== Next line is {line} ==")
        if line == "$ cd /":
            # print("Changing CWD to root")
            cwd = root
            parents.clear()
            continue
        if line == "$ cd ..":
            # print("Changing CWD to parent")
            cwd = parents.pop()
            continue
        if line.startswith("$ cd"):
            inner_dir_name = line.split()[2]
            # print(f"Changing CWD to { inner_dir_name }")
            parents.append(cwd)
            cwd = cwd[inner_dir_name]
            continue
        if line == "$ ls":
            continue
        assert not line.startswith("$")
        if line.startswith("dir"):
            cwd[line.split()[1]] = {}
            continue
        file_size, file_name = line.split()
        cwd[file_name] = int(file_size)

    return root


disk = parse_command_list(raw)


def parse_dir(dir_name, dir_content, accum):
    """Parse a single dictionary."""
    accum[dir_name] = 0
    for item_name, item_content in dir_content.items():
        if isinstance(item_content, int):
            accum[dir_name] += item_content
        else:
            inner_dir_name = dir_name + "." + item_name
            parse_dir(inner_dir_name, item_content, accum)  # Recurse!
            accum[dir_name] += accum[inner_dir_name]
    return accum


# Convert to flat dictionary of directory paths and sizes
dir_sizes = parse_dir("root", disk, {})

import cytoolz.curried as z

# Point-free golf
z.pipe(
    dir_sizes,
    z.valfilter(z.flip(int.__le__)(100_000)),
    dict.values,
    sum,
)

total_disk_size = 70_000_000
update_size = 30_000_000
min_space_to_delete = dir_sizes["root"] - (total_disk_size - update_size)
z.pipe(
    dir_sizes,
    dict.values,
    z.filter(z.flip(int.__ge__)(min_space_to_delete)),
    z.topk(1, key=int.__neg__),
)
