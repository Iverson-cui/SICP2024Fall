"""Homework 4: Data Abstraction and Trees"""

from ADT import tree, label, branches, is_leaf, print_tree, copy_tree
import doctest

#####################
# Required Problems #
#####################


# Problem 1
def couple(lst1, lst2):
    """Return a list that contains lists with i-th elements of two sequences
    coupled together.
    >>> lst1 = [1, 2, 3]
    >>> lst2 = [4, 5, 6]
    >>> couple(lst1, lst2)
    [[1, 4], [2, 5], [3, 6]]
    >>> lst3 = ['c', 6]
    >>> lst4 = ['s', '1']
    >>> couple(lst3, lst4)
    [['c', 's'], [6, '1']]
    """
    assert len(lst1) == len(lst2)
    result = [[x, y] for x in lst1 for y in lst2 if lst1.index(x) == lst2.index(y)]
    return result


# Problem 2
# The constructor and selectors of the arm


# constructor of mobile
def mobile(left, right):
    """Construct a mobile from a left arm and a right arm."""
    assert is_arm(left), "left must be a arm"
    assert is_arm(right), "right must be a arm"
    return ["mobile", left, right]


# judgment function for mobile
def is_mobile(m):
    """Return whether m is a mobile."""
    return type(m) == list and len(m) == 3 and m[0] == "mobile"


# left selector for mobile
def left(m):
    """Select the left arm of a mobile."""
    assert is_mobile(m), "must call left on a mobile"
    return m[1]


# right selector for mobile
def right(m):
    """Select the right arm of a mobile."""
    assert is_mobile(m), "must call right on a mobile"
    return m[2]


# arm constructor
def arm(length, mobile_or_planet):
    """Construct a arm: a length of rod with a mobile or planet at the end."""
    assert is_mobile(mobile_or_planet) or is_planet(mobile_or_planet)
    return ["arm", length, mobile_or_planet]


# judgment function for arm
def is_arm(s):
    """Return whether s is a arm."""
    return type(s) == list and len(s) == 3 and s[0] == "arm"


# length selector for arm
def length(s):
    """Select the length of a arm."""
    assert is_arm(s), "must call length on a arm"
    return s[1]


# end selector for arm
def end(s):
    """Select the mobile or planet hanging at the end of a arm."""
    assert is_arm(s), "must call end on a arm"
    return s[2]


# Problem 2.1
# constructor of planet
def planet(size):
    """Construct a planet of some size.

    >>> planet(5)
    ['planet', 5]
    """
    assert size > 0
    return ["planet", size]


def size(w):
    """Select the size of a planet.

    >>> p = planet(5)
    >>> size(p)
    5
    """
    assert is_planet(w), "must call size on a planet"
    return w[1]


def is_planet(w):
    """Whether w is a planet."""
    return type(w) == list and len(w) == 2 and w[0] == "planet"


# examples and usage
def examples():
    t = mobile(arm(1, planet(2)), arm(2, planet(1)))
    u = mobile(arm(5, planet(1)), arm(1, mobile(arm(2, planet(3)), arm(3, planet(2)))))
    v = mobile(arm(4, t), arm(2, u))
    return (t, u, v)


def total_weight(m):
    """Return the total weight of m, a planet or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    """
    assert is_mobile(m) or is_planet(m), "m must be a mobile or planet"
    if is_planet(m):
        return size(m)
    else:
        return total_weight(end(left(m))) + total_weight(end(right(m)))


# Problem 2.2
def balanced(m):
    """Return whether m is balanced.
    t 3 u 6 v 9 w 9

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(arm(3, t), arm(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(arm(1, v), arm(1, w)))
    False
    >>> balanced(mobile(arm(1, w), arm(1, v)))
    False
    """
    assert is_mobile(m)
    first_layer = length(left(m)) * total_weight(end(left(m))) == length(
        right(m)
    ) * total_weight(end(right(m)))
    if is_mobile(end(left(m))):
        left_one = balanced(end(left(m)))
    else:
        left_one = True
    if is_mobile(end(right(m))):
        right_one = balanced(end(right(m)))
    else:
        right_one = True

    return first_layer and left_one and right_one


# Problem 2.3
def totals_tree(m):
    """Return a tree representing the mobile/planet with its total weight at the root.

    >>> t, u, v = examples()
    >>> print_tree(totals_tree(t))
    3
      2
      1
    >>> print_tree(totals_tree(u))
    6
      1
      5
        3
        2
    >>> print_tree(totals_tree(v))
    9
      3
        2
        1
      6
        1
        5
          3
          2
    """
    assert is_mobile(m) or is_planet(m)
    root = total_weight(m)
    if is_planet(m):
        return tree(root)
    else:
        left_branch = totals_tree(end(left(m)))
        right_branch = totals_tree(end(right(m)))
        return tree(root, [left_branch, right_branch])


# Problem 3.1
def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    if is_leaf(t1) and is_leaf(t2):
        return tree(label(t1) + label(t2))
    else:
        final_branch = []
        len_branch1 = len(branches(t1))
        len_branch2 = len(branches(t2))
        max_length = max(len_branch1, len_branch2)
        for i in range(max_length):
            if i < len_branch1 and i < len_branch2:
                final_branch.append(add_trees(branches(t1)[i], branches(t2)[i]))
            elif i < len_branch1:
                final_branch.append(copy_tree(branches(t1)[i]))
            elif i < len_branch2:
                final_branch.append(copy_tree(branches(t2)[i]))
        return tree(label(t1) + label(t2), final_branch)


# Problem 3.2
# bigpath require that the path must traverse the root of the tree.
def bigpath(t, n):
    """Return the number of paths in t that have a sum larger or equal to n.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> bigpath(t, 3)
    4
    >>> bigpath(t, 6)
    2
    >>> bigpath(t, 9)
    1
    """
    # base case
    if is_leaf(t):
        return 1 if label(t) >= n else 0
    else:

        return (
            bigpath(branches(t)[0], n - label(t))
            + bigpath(branches(t)[1], n - label(t))
            + (label(t) >= n)
        )


# Problem 3.3
def bigger_path(t, n):
    """Return the number of paths in t that have a sum larger or equal to n.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> bigger_path(t, 3)
    9
    >>> bigger_path(t, 6)
    4
    >>> bigger_path(t, 9)
    1
    """
    path_containing_root = bigpath(t, n)
    if is_leaf(t):
        return path_containing_root
    else:
        sum_paths = path_containing_root
        for branch in branches(t):
            sum_paths += bigger_path(branch, n)
        return sum_paths


# Problem 3.4
def has_path(t, word):
    """Return whether there is a path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path(greetings, 'h')
    True
    >>> has_path(greetings, 'i')
    False
    >>> has_path(greetings, 'hi')
    True
    >>> has_path(greetings, 'hello')
    True
    >>> has_path(greetings, 'hey')
    True
    >>> has_path(greetings, 'bye')
    False
    """
    assert len(word) > 0, "no path for empty word."
    if is_leaf(t) or len(word) == 1:
        return label(t) == word
    elif label(t) == word[0]:
        for branch in branches(t):
            if has_path(branch, word[1:]):
                return True
    else:
        return False


##########################
# Just for fun Questions #
##########################


# Problem 4
def fold_tree(t, base_func, merge_func):
    """Fold tree into a value according to base_func and merge_func"""
    if is_leaf(t):
        return base_func(t)
    return base_func(t) + sum([merge_func(b) for b in branches(t)])


def count_leaves(t):
    """Count the leaves of a tree.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> count_leaves(t)
    3
    """
    return fold_tree(t, is_leaf, count_leaves)


def label_sum(t):
    """Sum up the labels of all nodes in a tree.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> label_sum(t)
    15
    """
    return fold_tree(t, label, label_sum)


def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal.

    >>> t = tree(1, [tree(2), tree(3, [tree(4), tree(5)])])
    >>> preorder(t)
    [1, 2, 3, 4, 5]
    """
    return fold_tree(t, lambda x: [label(x)], preorder)


def has_path_fold(t, word):
    """Return whether there is a path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path_fold(greetings, 'h')
    True
    >>> has_path_fold(greetings, 'i')
    False
    >>> has_path_fold(greetings, 'hi')
    True
    >>> has_path_fold(greetings, 'hello')
    True
    >>> has_path_fold(greetings, 'hey')
    True
    >>> has_path_fold(greetings, 'bye')
    False
    """
    assert len(word) > 0, "no path for empty word."
    return fold_tree(t, "YOUR EXPRESSION HERE", "YOUR EXPRESSION HERE")


if __name__ == "__main__":
    doctest.run_docstring_examples(preorder, globals(), verbose=True)
