"""Homework 5: Nonlocal and Generators"""

from ADT import tree, label, branches, is_leaf, print_tree

import doctest

#####################
# Required Problems #
#####################


def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> error = w(90, 'hax0r')
    >>> error
    'Insufficient funds'
    >>> error = w(25, 'hwat')
    >>> error
    'Incorrect password'
    >>> new_bal = w(25, 'hax0r')
    >>> new_bal
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> type(w(10, 'l33t')) == str
    True
    """
    password_attempts = []

    def withdraw(amount, password_attempt):
        nonlocal balance
        if len(password_attempts) >= 3:
            return f"Your account is locked. Attempts: {password_attempts}"
        if (password_attempt != password) and (
            password_attempt not in password_attempts
        ):
            password_attempts.append(password_attempt)
            return "Incorrect password"
        if amount > balance:
            return "Insufficient funds"
        balance -= amount
        return balance

    return withdraw


# When a client is connected to multiple passwords, we direct the function finally to calling the original withdraw function with the old password.
def make_joint(withdraw, old_pass, new_pass):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    """

    def joint_withdraw(balance, new_password_attempt):
        if new_password_attempt == new_pass:
            return withdraw(balance, old_pass)
        else:
            return withdraw(balance, new_password_attempt)

    # check if the old password is correct first
    # when balance is 0, returning a string means locked or incorrect password
    if type(withdraw(0, old_pass)) == str:
        return withdraw(0, old_pass)
    return joint_withdraw


def permutations(seq):
    """Generates all permutations of the given sequence. Each permutation is a
    list of all elements in seq. The permutations could be yielded in any order.

    >>> perms = permutations([100])
    >>> type(perms)
    <class 'generator'>
    >>> next(perms)
    [100]
    >>> try: #this piece of code prints "No more permutations!" if calling next would cause an error
    ...     next(perms)
    ... except StopIteration:
    ...     print('No more permutations!')
    No more permutations!
    >>> sorted(permutations([1, 2, 3])) # Returns a sorted list containing elements of the generator
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    if len(seq) == 0:
        yield []
    elif len(seq) == 1:
        yield [seq[0]]
    else:
        # permutations_except_first is a sequence of sequences containing all permutations of seq[1:]
        permutations_except_first = permutations(seq[1:])
        # insert seq[0] into each position of each perm.
        for perm in permutations_except_first:
            # in_place_mod_perm=perm[:]
            for i in range(len(perm) + 1):
                yield perm[:i] + [seq[0]] + perm[i:]


def two_sum_pairs(target, pairs):
    """Return True if there is a pair in pairs that sum to target."""
    # Tuple unpacking, unpack a pair (i,j).
    for i, j in pairs:
        if i + j == target:
            return True
    return False


def pairs(lst):
    """Yield the search space for two_sum_pairs.

    >>> two_sum_pairs(1, pairs([1, 3, 3, 4, 4]))
    False
    >>> two_sum_pairs(8, pairs([1, 3, 3, 4, 4]))
    True
    >>> lst = [1, 3, 3, 4, 4]
    >>> plst = pairs(lst)
    >>> n, pn = len(lst), len(list(plst))
    >>> n * (n - 1) / 2 == pn
    True
    """
    # yield a pair (i,j) by "yield i,j"
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            yield lst[i], lst[j]


def two_sum_list(target, lst):
    """Return True if there are two different elements in lst that sum to target.

    >>> two_sum_list(1, [1, 3, 3, 4, 4])
    False
    >>> two_sum_list(8, [1, 3, 3, 4, 4])
    True
    >>> two_sum_list(8, [4])
    False
    >>> two_sum_list(8, [4, 4])
    True
    """
    visited = []
    for val in lst:
        if target - val in visited:
            return True
        visited.append(val)

    return False


# return many generators
def lookups(k, key):
    """Yield one lookup function for each node of k that has the label key.
    >>> k = tree(5, [tree(7, [tree(2)]), tree(8, [tree(3), tree(4)]), tree(5, [tree(4), tree(2)])])
    >>> v = tree('Go', [tree('C', [tree('C')]), tree('A', [tree('S'), tree(6)]), tree('L', [tree(1), tree('A')])])
    >>> type(lookups(k, 4))
    <class 'generator'>
    >>> sorted([f(v) for f in lookups(k, 2)])
    ['A', 'C']
    >>> sorted([f(v) for f in lookups(k, 3)])
    ['S']
    >>> [f(v) for f in lookups(k, 6)]
    []
    """
    # yield functions that takes input tree v return labels in v.

    # # yield a tree combining labels of k and v
    # def tree_dictionary(v, k):
    #     """Your existing function - this works fine"""
    #     if is_leaf(k) and is_leaf(v):
    #         return tree({"key": label(k), "value": label(v)})
    #     return tree(
    #         label={"key": label(k), "value": label(v)},
    #         branches=[
    #             tree_dictionary(v_branch, k_branch)
    #             for v_branch, k_branch in zip(branches(v), branches(k))
    #         ],
    #     )

    # a function that continuously yield path from root to nodes with target key.
    # [] means root. [1] means 1st branch from root, [12] means 2nd branch of 1st branch from root, etc.

    # use list to keep track of the paths you have taken.
    def find_paths_to_key(tree, target_key, current_path=[]):
        """Find all paths to nodes with the target key"""
        if label(tree) == target_key:
            yield current_path[:]  # Found a matching node, yield the path

        for i, branch in enumerate(branches(tree)):
            yield from find_paths_to_key(branch, target_key, current_path + [i])

    # given a path, like [32311], then given a tree v, traverse the tree following the path, return the label of the node at that path.
    def make_lookup_function(path):
        """Create a lookup function for a specific path"""

        def lookup_function(v):
            # Navigate to the corresponding position in v using the path
            current = v
            for index in path:
                if index < len(branches(current)):
                    current = branches(current)[index]
                else:
                    return None  # Path doesn't exist in v
            return label(current)

        return lookup_function

    # Find all paths to nodes with the target key and yield lookup functions
    for path in find_paths_to_key(k, key):
        yield make_lookup_function(path)


##########################
# Just for fun Questions #
##########################


# input int, output a generator, which sequentially yields generators. the yielded generators yield natural numbers.
def remainders_generator(m):
    """Yields m generators. The ith yielded generator yields natural numbers whose
    remainder is i when divided by m.

    >>> import types
    >>> [isinstance(gen, types.GeneratorType) for gen in remainders_generator(5)]
    [True, True, True, True, True]
    >>> remainders_four = remainders_generator(4)
    >>> for i in range(4):
    ...     print("First 3 natural numbers with remainder {0} when divided by 4:".format(i))
    ...     gen = next(remainders_four)
    ...     for _ in range(3):
    ...         print(next(gen))
    First 3 natural numbers with remainder 0 when divided by 4:
    0
    4
    8
    First 3 natural numbers with remainder 1 when divided by 4:
    1
    5
    9
    First 3 natural numbers with remainder 2 when divided by 4:
    2
    6
    10
    First 3 natural numbers with remainder 3 when divided by 4:
    3
    7
    11
    """

    # remainder_generator(remainder) itself is a generator.
    def remainder_generator(remainder):
        """Yields natural numbers with a specific remainder when divided by m."""
        n = remainder
        while True:
            yield n
            n += m

    for i in range(m):
        yield remainder_generator(i)


def starting_from(start):
    """Yields natural numbers starting from start.

    >>> sf = starting_from(0)
    >>> [next(sf) for _ in range(10)] == list(range(10))
    True
    """
    yield start
    yield from starting_from(start + 1)


def sieve(t):
    """Suppose the smallest number from t is p, sieves out all the
    numbers that can be divided by p (except p itself) and recursively
    sieves out all the multiples of the next smallest number from the
    reset of of the sequence.

    >>> list(sieve(iter([3, 4, 5, 6, 7, 8, 9])))
    [3, 4, 5, 7]
    >>> list(sieve(iter([2, 3, 4, 5, 6, 7, 8])))
    [2, 3, 5, 7]
    >>> list(sieve(iter([1, 2, 3, 4, 5])))
    [1]
    """
    t = list(t)

    if t == [1]:
        return [1]
    if not t:
        return []
    p = min(t)
    yield p
    remaining = [x for x in t if x % p != 0]

    yield from sieve(iter(remaining))


# list(sieve(iter([3, 4, 5, 6, 7, 8, 9])))


def primes():
    """Yields all the prime numbers.

    >>> p = primes()
    >>> [next(p) for _ in range(10)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    yield from sieve(iter(range(2, 100)))  # You can change the range limit as needed


if __name__ == "__main__":
    doctest.run_docstring_examples(primes, globals(), verbose=True)
