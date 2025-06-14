"""Lab 3: Recursion"""

import doctest

LAB_SOURCE_FILE = "lab03.py"


# ANSWER QUESTION q1

# ANSWER QUESTION q2

# ANSWER QUESTION q3


def f91(n):
    """Takes a number n and returns n - 10 when n > 100,
    returns f91(f91(n + 11)) when n ≤ 100.

    >>> f91(1)
    91
    >>> f91(2)
    91
    >>> f91(100)
    91
    """
    return n - 10 if n > 100 else f91(f91(n + 11))


def is_monotone(n):
    """Returns whether n has monotone digits.
    Implement using recursion!

    >>> is_monotone(22000130)
    False
    >>> is_monotone(1234)
    True
    >>> is_monotone(24555)
    True
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(LAB_SOURCE_FILE, 'is_monotone', ['While', 'For'])
    True
    """
    # only one digit left
    if n // 10 == 0:
        return True
    else:
        last_digit = n % 10
        next_digit = n // 10 % 10
        if last_digit >= next_digit:
            # if the last digit is greater than or equal to the next digit,
            # we can continue checking the rest of the digits
            return is_monotone(n // 10)
        else:
            return False


def count_stair_ways(n):
    """Returns the number of ways to climb up a flight of
    n stairs, moving either 1 step or 2 steps at a time.
    >>> count_stair_ways(3)
    3
    >>> count_stair_ways(4)
    5
    >>> count_stair_ways(10)
    89
    """
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        # The number of ways to reach the nth step is the sum of the ways to reach
        # the (n-1)th step and the (n-2)th step.
        return count_stair_ways(n - 1) + count_stair_ways(n - 2)


# base case is: count_k(0,0) and count_k(1,1) both return 1
# consider how he gets to where he is now, meaning what the last step is: based on that we have the next layer of leaves of our recursive tree.
# when n<k, (n,k) equals to (n,n)


def count_k(n, k):
    """Counts the number of paths to climb up a flight of n stairs,
    taking up to and including k steps at a time.
    >>> count_k(3, 3) # 3, 2 + 1, 1 + 2, 1 + 1 + 1
    4
    >>> count_k(4, 4)
    8
    >>> count_k(10, 3)
    274
    >>> count_k(300, 1) # Only one step at a time
    1
    >>> count_k(3, 5) # Take no more than 3 steps
    4
    """
    if (n == 1 and k == 1) or (n == 0 and k == 0):
        return 1
    elif n < k:
        return count_k(n, n)
    else:
        return sum(count_k(n - i, k) for i in range(1, k + 1))


def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    if m == 1 or n == 1:
        return 1

    else:
        # The number of paths to the bottom-right corner is the sum of the paths
        # from the cell directly above and the cell directly to the left.
        return paths(m - 1, n) + paths(m, n - 1)


def max_subseq(n, l):
    """
    Return the maximum subsequence of length at most l that can be found in the given number n.
    For example, for n = 20125 and l = 3, we have that the subsequences are
        2
        0
        1
        2
        5
        20
        21
        22
        25
        01
        02
        05
        12
        15
        25
        201
        202
        205
        212
        215
        225
        012
        015
        025
        125
    and of these, the maximum number is 225, so our answer is 225.

    >>> max_subseq(20125, 3)
    225
    >>> max_subseq(20125, 5)
    20125
    >>> max_subseq(20125, 6) # note that 20125 == 020125
    20125
    >>> max_subseq(12345, 3)
    345
    >>> max_subseq(12345, 0) # 0 is of length 0
    0
    >>> max_subseq(12345, 1)
    5
    """
    if n // 10 == 0 and l == 1:
        return n
    elif n // 10 == 0 and l > 1:
        return n
    elif l == 0:
        return 0
    else:
        return max(10 * max_subseq(n // 10, l - 1) + n % 10, max_subseq(n // 10, l))


# There are two key insights for this problem:

# You need to split into two cases, the one where the last digit is used and the one where it is not. In the case where it is, we want to reduce l since we used the last digit, and in the case where it isn't, we do not.
# In the case where we are using the last digit, you need to put the digit back onto the end, and the way to attach a digit d to the end of a number n is 10 * n + d.

if __name__ == "__main__":
    doctest.run_docstring_examples(max_subseq, globals(), verbose=True)
