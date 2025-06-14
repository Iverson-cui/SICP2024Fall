"""Homework 2: Higher-Order Functions"""

import doctest

from operator import add, mul, sub

square = lambda x: x * x
identity = lambda x: x
triple = lambda x: 3 * x
increment = lambda x: x + 1


#####################
# Required Problems #
#####################


def compose(h, g):
    """Return a function f, such that f(x) = h(g(x)).

    >>> compose(square, triple)(5)
    225
    >>> double_inc = compose(increment, increment)
    >>> double_inc(3)
    5
    >>> double_inc(4)
    6
    """
    return lambda x: h(g(x))


def product(n, f):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    f -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    result = 1
    for i in range(1, n + 1):
        result = mul(result, f(i))
    return result


def accumulate(combiner, base, n, f):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are f(1), f(2), ..., f(n).  combiner is a
    two-argument commutative, associative function.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    >>> accumulate(lambda x, y: (x + y) % 17, 19, 20, square)
    16
    """
    result = base
    for i in range(1, n + 1):
        result = combiner(result, f(i))
    return result


def summation_using_accumulate(n, f):
    """Returns the sum of f(1) + ... + f(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check('hw02.py', 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(add, 0, n, f)


def product_using_accumulate(n, f):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check('hw02.py', 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(mul, 1, n, f)


def missions(f):
    """DO NOT EDIT THIS FUNCTION"""

    def mission1(f):
        if f(0) == 0 and f(1) == 2:
            print("MISSION 1 SOLVED")
            return lambda g: mission2(g(f))
        else:
            print("MISSION 1 FAILED")

    def mission2(f):
        if f(0) == 0 and f(1) == 2:
            print("MISSION 2 SOLVED")
            return mission3(0, 0)
        else:
            print("MISSION 2 FAILED")

    def mission3(f, g):
        def mission3_inner(f):
            if f == g:
                return mission3(f, g + 1)

        if g == 5:
            print("MISSION 3 SOLVED")
            return "The cake is a lie."
        else:
            return mission3_inner

    return mission1(f)


def get_the_cake(missions):
    """
    Write a higher order function so that it calls three
    mission functions in turn and return the hidden cake.
    You are not allowed to return variable cake or print
    the messages directly. A correct solution contains
    only one expression.

    By the way, do you know that "The cake is a lie" is
    a catchphrase from the 2007 video game Portal? Visit
    https://en.wikipedia.org/wiki/The_cake_is_a_lie
    if you have never played Portal before!

    >>> the_cake = get_the_cake(missions)
    MISSION 1 SOLVED
    MISSION 2 SOLVED
    MISSION 3 SOLVED
    >>> the_cake
    'The cake is a lie.'
    >>> # check that your answer consists of nothing but an
    >>> # expression (this docstring) and a return statement
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(get_the_cake)).body[0].body]
    ['Expr', 'Return']
    """
    return missions(lambda x: mul(x, 2))(identity)(0)(1)(2)(3)(4)


def protected_secret(password, secret, num_attempts):
    """
    Returns a function which takes in a password and prints the SECRET if the password entered matches
    the PASSWORD given to protected_secret. Otherwise it prints "INCORRECT PASSWORD". After NUM_ATTEMPTS
    incorrect passwords are entered, the secret is locked and the function should print "SECRET LOCKED".

    >>> my_secret = protected_secret("correcthorsebatterystaple", "I love NJU", 2)
    >>> # this my_secret's parent diagram is the function with num_attempts = 2
    >>> # Failed attempts: 0
    >>> my_secret = my_secret("hax0r_1")
    INCORRECT PASSWORD
    >>> # this my_secret's parent diagram is the function with num_attempts = 1
    >>> # Failed attempts: 1
    >>> my_secret = my_secret("correcthorsebatterystaple")
    I love NJU
    >>> my_secret = my_secret("correcthorsebatterystaple")
    I love NJU
    >>> # Failed attempts: 1
    >>> my_secret = my_secret("hax0r_2")
    INCORRECT PASSWORD
    >>> # Failed attempts: 2
    >>> my_secret = my_secret("hax0r_3")
    SECRET LOCKED
    >>> my_secret = my_secret("correcthorsebatterystaple")
    SECRET LOCKED
    """

    def get_secret(password_attempt):
        if num_attempts <= 0:
            print("SECRET LOCKED")
            return protected_secret(password, secret, num_attempts)
        elif password_attempt == password:
            print(secret)
            return protected_secret(password, secret, num_attempts)
        else:
            print("INCORRECT PASSWORD")
            return protected_secret(password, secret, num_attempts - 1)

    return get_secret


##########################
# Just for fun Questions #
##########################


# zero is a function. It accepts sth and returns a function A. A accepts sth and returns what it received.
# This means applying function f to x zero times
def zero(f):
    return lambda x: x


# successor is a function. It accepts a function n and returns a function A.
# A accepts a function f and returns B.
# B= f(n(f)(x)). n is what is passed into successor, first n(f) means n takes in a function. n(f)(x) means n also returns a function.
# n,f,n(f) are all functions.
def successor(n):
    return lambda f: lambda x: f(n(f)(x))


# successor(zero): zero is a function, successor(zero) is a function. so in this case n(f)(x) equals to x. lambda f: lambda x: f(x).
# So successor(zero) under the hood is a function that takes in two stages of arguments, one is function the other is the function argument, and return f(x)
# successor(zero) means applying function f to x one time. so one(f) = successor(zero)(f)
def one(f):
    """Church numeral 1: same as successor(zero)"""
    return lambda x: f(x)


# applying f to x two times.
def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    return lambda x: f(f(x))


three = successor(two)

# zero one two three in essence are functions that take in f and x, return f applied to x a certain number of times.


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(successor(three))
    4
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    # Use the Church numeral's property: n(increment)(0) gives us the integer
    return n(increment)(0)


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    >>> church_to_int(add_church(three, three))
    6
    >>> church_to_int(add_church(two, two))
    4
    """
    return lambda f: lambda x: n(f)(m(f)(x))


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.
    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    return lambda f: lambda x: m(n(f))(x)


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    >>> church_to_int(pow_church(three, three))
    27
    >>> church_to_int(pow_church(two, two))
    4
    """
    return n(m)


if __name__ == "__main__":
    doctest.run_docstring_examples(mul_church, globals(), verbose=True)

"""
This problem is about church numerals.the last three functions are worth our concentration. add, mult, and power. for example, three means carrying out function f three times to x. different situations require different f. Sometimes it's f, sometimes it's three(f), sometimes it's three, each with different meanings. 
x is also different. Takeaway is that in python, no type of variables is explicitly mentioned so every variable could be everything, like x here could be a function.

"""
