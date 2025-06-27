"""Lab 07: Special Method, Linked Lists and Mutable Trees"""

# ANSWER QUESTION q1

# ANSWER QUESTION q2

# ANSWER QUESTION q3

#####################
# Required Problems #
#####################


class Complex:
    """Complex Number.

    >>> a = Complex(1, 2)
    >>> a
    Complex(real=1, imaginary=2)
    >>> print(a)
    1 + 2i
    >>> b = Complex(-1, -2)
    >>> b
    Complex(real=-1, imaginary=-2)
    >>> print(b)
    -1 + -2i
    >>> print(a + b)
    0 + 0i
    >>> print(a * b)
    3 + -4i
    >>> print(a)
    1 + 2i
    >>> print(b)    # a and b should not be changed
    -1 + -2i
    """

    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        return f"Complex(real={self.real}, imaginary={self.imaginary})"

    def __str__(self):
        return f"{self.real} + {self.imaginary}i"

    def __add__(self, other):
        """Return the sum of two complex numbers."""
        assert isinstance(other, Complex)
        return Complex(self.real + other.real, self.imaginary + other.imaginary)

    def __mul__(self, other):
        """Return the product of two complex numbers."""
        assert isinstance(other, Complex)
        real_part = self.real * other.real - self.imaginary * other.imaginary
        imaginary_part = self.real * other.imaginary + self.imaginary * other.real
        return Complex(real_part, imaginary_part)


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(0)
    >>> s
    Link(0)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(8760)
    Link(8, Link(7, Link(6, Link(0))))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not steal chicken!") if any([r in cleaned for r in ["str", "repr", "reversed"]]) else None
    """
    digits = []
    temp = n
    while temp > 0:
        digits.insert(0, temp % 10)
        temp //= 10

    # cases of 0
    if n == 0:
        return Link(0)
    # cases of single digit
    if len(digits) == 1:
        return Link(digits[0])
    return Link(digits[0], store_digits(n % 10 ** (len(digits) - 1)))


def deep_map_mut(func, link):
    """Mutates a deep link by replacing each item found with the
    result of calling func on the item. DO NOT create new Links (so
    no use of Link's constructor) and DO NOT return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not steal chicken!"), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    if link is Link.empty:
        return
    if isinstance(link.first, Link):
        deep_map_mut(func, link.first)
    else:
        # this is the base case
        link.first = func(link.first)
    deep_map_mut(func, link.rest)


def cumulative_mul(t):
    """Mutates t so that each node's label becomes the product of all labels in
    the corresponding subtree rooted at t.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> cumulative_mul(t)
    >>> t
    Tree(105, [Tree(15, [Tree(5)]), Tree(7)])
    """

    # Helper function to recursively calculate the product of labels
    # it returns the product of the current node's label and the products of all branches
    def helper(t):
        if t.is_leaf():
            return t.label
        branch_products = 1
        for b in t.branches:
            branch_products = branch_products * helper(b)
        return t.label * branch_products

    t.label = helper(t)
    for b in t.branches:
        cumulative_mul(b)


def prune_small(t, n):
    """Prune the tree mutatively, keeping only the n branches
    of each node with the smallest label.

    >>> t1 = Tree(6)
    >>> prune_small(t1, 2)
    >>> t1
    Tree(6)
    >>> t2 = Tree(6, [Tree(3), Tree(4)])
    >>> prune_small(t2, 1)
    >>> t2
    Tree(6, [Tree(3)])
    >>> t3 = Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2), Tree(3)]), Tree(5, [Tree(3), Tree(4)])])
    >>> prune_small(t3, 2)
    >>> t3
    Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])
    """

    # branches is a list, we can use list.pop to remove elements from it.
    # num means how many branches we need to prune
    def prune_helper(t, num):
        if t.is_leaf():
            return
        # if len(t.branches) <= num:
        #     return
        label_lst = []
        for b in t.branches:
            # label_lst contains all of the labels of the branches
            label_lst.append(b.label)
        for _ in range(num):
            max_index = label_lst.index(max(label_lst))
            t.branches.pop(max_index)
        return

    if t.is_leaf():
        return
    num_before = len(t.branches)
    prune_helper(t, num_before - n) if num_before > n else None
    for b in t.branches:
        prune_small(b, n)
    return


#####################
#        ADT        #
#####################


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """

    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ", " + repr(self.rest)
        else:
            rest_repr = ""
        return "Link(" + repr(self.first) + rest_repr + ")"

    def __str__(self):
        string = "<"
        while self.rest is not Link.empty:
            string += str(self.first) + " "
            self = self.rest
        return string + str(self.first) + ">"


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ", " + repr(self.branches)
        else:
            branch_str = ""
        return "Tree({0}{1})".format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = "  " * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str

        return print_tree(self).rstrip()
