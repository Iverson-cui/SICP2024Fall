"""Homework 3: Recursion"""

import doctest

HW_SOURCE_FILE = "hw03.py"


#####################
# Required Problems #
#####################


def integrate(f, l, r, min_interval):
    """Return the definite integration of function f over interval
    [l,r], with interval length limit min_interval.

    >>> abs(integrate(lambda x: x * x, 1, 2, 0.01) - (7 / 3)) < 0.001
    True
    >>> abs(integrate(lambda x: x, 1, 2, 0.01) - 1.5) < 0.0001
    True
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'integrate', ['While', 'For'])
    True
    """

    def trapezoid_area(f, a, b):
        """Return the area of the trapezoid under f between a and b."""
        return (f(a) + f(b)) * (b - a) / 2

    if r - l < min_interval:
        return trapezoid_area(f, l, r)
    else:
        return integrate(f, l, (l + r) / 2, min_interval) + integrate(
            f, (l + r) / 2, r, min_interval
        )


def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    5
    >>> pingpong(8)
    4
    >>> pingpong(15)
    3
    >>> pingpong(21)
    5
    >>> pingpong(22)
    6
    >>> pingpong(30)
    10
    >>> pingpong(68)
    0
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    -1
    >>> pingpong(72)
    -2
    >>> pingpong(100)
    6
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """

    def contains_six(n):
        """Returns whether n contains the digit 6."""
        while n > 0:
            if n % 10 == 6:
                return True
            n //= 10
        return False

    # returns the direction of the sequence at index n. 1 for increase and -1 for decrease.
    def switch_direction(index, direction):
        """Switch the direction of the ping-pong sequence."""
        if index % 6 == 0 or contains_six(index):
            return -direction
        return direction

    def pingpong_helper(index, current_value, current_direction, target):
        if index == target:
            return current_value
        return pingpong_helper(
            index + 1,
            current_value + current_direction,
            switch_direction(index + 1, current_direction),
            target,
        )

    return pingpong_helper(1, 1, 1, n)


# The recursive function can start at base case once a limitation is given in the input argument of the function. In this case, pingpong_helper is such a function, with targets the limitation.


def balanced(s):
    """Returns whether the given parentheses sequence s is balanced.
    >>> balanced('()')
    True
    >>> balanced(')')
    False
    >>> balanced('(())')
    True
    >>> balanced('()()')
    True
    >>> balanced('()())')
    False
    >>> balanced('()(()')
    False
    """

    def divide(s, k):
        """Divide the given parentheses sequence s into two parts at position k.
        >>> left, right = divide('()()', 2)
        >>> left
        '()'
        >>> right
        '()'
        >>> left, right = divide('(())()', 4)
        >>> left
        '(())'
        >>> right
        '()'
        >>> left, right = divide('(())()', 6)
        >>> left
        '(())()'
        >>> right
        ''
        """
        return (s[:k], s[k:])

    def peel(s):
        """Peel off the leftmost and rightmost parentheses in s to obtain the
        internal part of the parentheses sequence.
        >>> peel('(())')
        '()'
        >>> peel('()')
        ''
        >>> peel('))((')
        ')('
        """
        return s[1:-1]

    # Check if the leftmost and rightmost parentheses in s match. If don't, return False.
    def match(s):
        """Returns whether the leftmost and the rightmost parentheses in s match.
        >>> match('()')
        True
        >>> match('()()')
        True
        >>> match('()))')
        True
        >>> match('))')
        False
        >>> match(')())')
        False
        """
        return s[0] == "(" and s[-1] == ")"

    def divide_position(s):
        left, right = 0, 0
        for char in s:
            if char == "(":
                left += 1
            elif char == ")":
                right += 1
            # The sequence can be divided in the middle.
            if (left == right) and (left + right != 0):
                return left + right
        # if all of the char in s is iterated, condition is not met, then sequence s has mismatching parentheses.
        return -1

    if s == "":
        return True
    pos = divide_position(s)
    if (pos == -1) or (match(s) is False):
        return False

    if pos == len(s):
        return balanced(peel(s))
    else:
        left_s, right_s = divide(s, pos)
        return balanced(left_s) and balanced(right_s)


# if the max money denomination is larger than total, that denomination can be discarded. In case money is some functions without bound, we have to find what corresponds to the denomination that can be used.
def max_index(total, money):
    """Return the maximum index of money that can be used to make change for total."""
    i = 1
    while True:
        if (money(i) is None) or (money(i) > total):
            return i - 1
        i += 1


def chinese_yuan(ith):
    if ith == 1:
        return 1
    if ith == 2:
        return 5
    if ith == 3:
        return 10
    if ith == 4:
        return 20
    if ith == 5:
        return 50
    if ith == 6:
        return 100


def count_change(total, money):
    """Return the number of ways to make change for total,
    under the currency system described by money.

    >>> def chinese_yuan(ith):
    ...     if ith == 1:
    ...         return 1
    ...     if ith == 2:
    ...         return 5
    ...     if ith == 3:
    ...         return 10
    ...     if ith == 4:
    ...         return 20
    ...     if ith == 5:
    ...         return 50
    ...     if ith == 6:
    ...         return 100
    >>> def us_cent(ith):
    ...     if ith == 1:
    ...         return 1
    ...     if ith == 2:
    ...         return 5
    ...     if ith == 3:
    ...         return 10
    ...     if ith == 4:
    ...         return 25
    >>> count_change(15, chinese_yuan)
    6
    >>> count_change(49, chinese_yuan)
    44
    >>> count_change(49, us_cent)
    39
    >>> count_change(49, lambda x: 2 ** (x - 1))
    692
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_change', ['While', 'For'])
    True
    """

    # def count_helper(total, money, index):
    #     if total == 0:
    #         return 1
    #     if total < 0 or index == 0:
    #         return 0
    #     return count_helper(total - money(index), money, index) + count_helper(total, money, index - 1)

    def count_helper(total, money):
        max_idx = max_index(total, money)

        if total == 0:
            return 1
        if total < 0:
            return 0
        if max_idx == 0:
            return 0
        return count_helper(total - money(max_idx), money) + count_helper(
            total, lambda x: money(x) if x < max_idx else None
        )

    return count_helper(total, money)


# count_change(15, chinese_yuan)  # Example usage to test the function


def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)


def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    mid = 6 - start - end
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    if n == 1:
        return print_move(
            start, end
        )  # Base case: if there's only one disk, move it directly.
    if n > 1:
        move_stack(n - 1, start, mid)
        move_stack(1, start, end)
        move_stack(n - 1, mid, end)


def multiadder(n):
    """Return a function that takes N arguments, one at a time, and adds them.
    >>> f = multiadder(3)
    >>> f(5)(6)(7) # 5 + 6 + 7
    18
    >>> multiadder(1)(5)
    5
    >>> multiadder(2)(5)(6) # 5 + 6
    11
    >>> multiadder(4)(5)(6)(7)(8) # 5 + 6 + 7 + 8
    26
    >>> from construct_check import check
    >>> # Make sure multiadder is a pure function.
    >>> check(HW_SOURCE_FILE, 'multiadder',
    ...       ['Nonlocal', 'Global'])
    True
    """

    def adder(result, x, n):
        if n == 1:
            return result + x
        else:
            return lambda next: adder(result + x, next, n - 1)

    return lambda x: adder(0, x, n)


##########################
# Just for fun Questions #
##########################


from operator import sub, mul


def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return lambda n: (lambda f, x: 1 if x == 1 else mul(x, f(f, sub(x, 1))))(
        lambda f, x: 1 if x == 1 else mul(x, f(f, sub(x, 1))), n
    )


def Y(f):
    return (lambda x: x(x))(lambda x: f(lambda z: x(x)(z)))


def fib_maker(f):
    return lambda r: "YOUR_EXPRESSION_HERE"


def number_of_six_maker(f):
    return lambda r: "YOUR_EXPRESSION_HERE"


my_fib = Y(fib_maker)
my_number_of_six = Y(number_of_six_maker)

# This code sets up doctests for my_fib and my_number_of_six.

my_fib.__name__ = "my_fib"
my_fib.__doc__ = """Given n, returns the nth Fibonacci nuimber.

>>> my_fib(0)
0
>>> my_fib(1)
1
>>> my_fib(2)
1
>>> my_fib(3)
2
>>> my_fib(4)
3
>>> my_fib(5)
5
"""

my_number_of_six.__name__ = "my_number_of_six"
my_number_of_six.__doc__ = """Return the number of 6 in each digit of a positive integer n.

>>> my_number_of_six(666)
3
>>> my_number_of_six(123456)
1
"""

if __name__ == "__main__":
    doctest.run_docstring_examples(make_anonymous_factorial, globals(), verbose=True)
