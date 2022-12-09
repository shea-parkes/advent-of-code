import cytoolz.curried as z
import numpy as np

with open("input.txt") as fh_in:
    raw = fh_in.read()


trees = z.pipe(
    raw,
    str.split,
    z.map(
        z.compose_left(
            z.map(int),
            list,
        )
    ),
    list,
    np.array,
)
assert trees.shape[0] == trees.shape[1]


def determine_visibility(row):
    """Determine visibility of the row"""
    max_height = -1
    visibility = []
    for tree in row:
        visibility.append(tree > max_height)
        max_height = max(tree, max_height)
    return np.array(visibility)


visibility_masks = []
for angle in range(4):
    spun = np.rot90(trees, angle)
    visibility_spun = np.apply_along_axis(determine_visibility, 0, spun)
    visibility_orig = np.rot90(visibility_spun, 4 - angle)
    visibility_masks.append(visibility_orig)

visibility_mask = z.reduce(np.logical_or, visibility_masks)
np.sum(visibility_mask)
