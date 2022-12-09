import operator as op

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


@z.curry
def apply_in_all_directions(func, arr):
    """Apply a row-wise function in all four directions"""

    def rotate_and_apply(n_rotations):
        """Inner closure"""
        return z.pipe(
            arr,
            z.partial(np.rot90, k=n_rotations),
            z.partial(np.apply_along_axis, func, 0),
            z.partial(np.rot90, k=4 - n_rotations),
        )

    return z.pipe(
        range(4),
        z.map(rotate_and_apply),
    )


def determine_visibility(row):
    """Determine visibility of a given row"""
    max_height = -1
    visibility = []
    for tree in row:
        visibility.append(tree > max_height)
        max_height = max(tree, max_height)
    return np.array(visibility)


z.pipe(
    trees,
    apply_in_all_directions(determine_visibility),
    z.reduce(np.logical_or),
    np.sum,
)


def calc_scenic_scores(row):
    """Determine scenic scores of the row"""
    prior_trees = []
    scenic_scores = []
    for tree in row:
        scenic_score = 0
        for reversed_tree in reversed(prior_trees):
            scenic_score += 1
            if reversed_tree >= tree:
                break
        scenic_scores.append(scenic_score)
        prior_trees.append(tree)
    return np.array(scenic_scores)


z.pipe(
    trees,
    apply_in_all_directions(calc_scenic_scores),
    z.reduce(np.multiply),
    np.max,
)
