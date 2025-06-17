# ANSWER QUESTION wwpd

import itertools
import doctest


def takeWhile(t, p):
    """Take elements from t until p is not satisfied.

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> list(takeWhile(s, lambda x: x == 10))
    [10]
    >>> s2 = iter([1, 1, 2, 3, 5, 8, 13])
    >>> list(takeWhile(s2, lambda x: x % 2 == 1))
    [1, 1]
    >>> s = iter(['a', '', 'b', '', 'c'])
    >>> list(takeWhile(s, lambda x: x != ''))
    ['a']
    >>> list(takeWhile(s, lambda x: x != ''))
    ['b']
    >>> next(s)
    'c'
    """
    # t1, t2 = itertools.tee(t)
    # result = []
    # while p(next(t1)):
    #     result.append(next(t2))
    # next(t2)
    # return result

    result = []
    for item in t:
        if p(item):
            result.append(item)
        else:
            # We need to put this item back somehow, but iterators don't support that
            # So we'd need a different approach
            break
    return result


# input t is an iterator, output is also an iterator.
def backAndForth(t):
    """Yields and skips elements from iterator t, back and forth.

    >>> list(backAndForth(iter([1, 2, 3, 4, 5, 6, 7, 8, 9])))
    [1, 4, 5, 6]
    >>> list(backAndForth(iter([1, 2, 2])))
    [1]
    >>> # generators allow us to represent infinite sequences!!!
    >>> def naturals():
    ...     i = 0
    ...     while True:
    ...         yield i
    ...         i += 1
    >>> m = backAndForth(naturals())
    >>> [next(m) for _ in range(9)]
    [0, 3, 4, 5, 10, 11, 12, 13, 14]
    """
    num = 1
    forth = 1
    while True:
        if forth:
            for _ in range(num):
                try:
                    yield next(t)
                except StopIteration:
                    return

        else:
            for _ in range(num):
                try:
                    next(t)
                except StopIteration:
                    return

        forth = not forth
        num += 1


def scale(it, multiplier):
    """Yield elements of the iterable it scaled by a number multiplier.

    >>> m = scale(iter([1, 5, 2]), 5)
    >>> type(m)
    <class 'generator'>
    >>> list(m)
    [5, 25, 10]
    >>> # generators allow us to represent infinite sequences!!!
    >>> def naturals():
    ...     i = 0
    ...     while True:
    ...         yield i
    ...         i += 1
    >>> m = scale(naturals(), 2)
    >>> [next(m) for _ in range(5)]
    [0, 2, 4, 6, 8]
    """
    yield from map(lambda x: x * multiplier, it)


def merge(a, b):
    """Merge two generators that are in increasing order and without duplicates.
    Return a generator that has all elements of both generators in increasing
    order and without duplicates.

    >>> def sequence(start, step):
    ...     while True:
    ...         yield start
    ...         start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]
    """
    # list_a = list(a)
    # list_b = list(b)
    # i, j = 0, 0
    # while i < len(list_a) and j < len(list_b):
    #     if list_a[i] < list_b[j]:
    #         yield list_a[i]
    #         i += 1
    #     elif list_a[i] > list_b[j]:
    #         yield list_b[j]
    #         j += 1
    #     else:  # they are equal
    #         yield list_a[i]
    #         i += 1
    #         j += 1
    # if i < len(list_a):
    #     yield from list_a[i:]
    # if j < len(list_b):
    #     yield from list_b[j:]
    a_next = next(a)
    b_next = next(b)
    while True:
        # a < b
        if a_next < b_next:
            yield a_next
            a_next = next(a)
        # a > b
        elif a_next > b_next:
            yield b_next
            b_next = next(b)
        elif a_next == b_next:
            yield a_next
            a_next = next(a)
            b_next = next(b)


def hailstone(n):
    """Return a generator that outputs the hailstone sequence.

    >>> for num in hailstone(10):
    ...     print(num)
    10
    5
    16
    8
    4
    2
    1
    """
    # while n != 1:
    #     yield n
    #     if n % 2 == 0:
    #         n //= 2
    #     else:
    #         n = 3 * n + 1
    # yield 1

    # Try using yield from and recursion
    yield n
    if n == 1:
        return
    elif n % 2 == 0:
        yield from hailstone(n // 2)
    else:
        yield from hailstone(3 * n + 1)


if __name__ == "__main__":
    doctest.run_docstring_examples(hailstone, globals(), verbose=True)
