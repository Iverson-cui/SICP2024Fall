test = {
  'name': 'Question 2',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> class A:
          ...     x, y = 0, 0
          ...     def __init__(self):
          ...          return
          >>> class B(A):
          ...     def __init__(self):
          ...          return
          >>> class C(A):
          ...     def __init__(self):
          ...          return
          >>> print(A.x, B.x, C.x)
          77e37f8d8d61249def70a846ac04b954
          # locked
          >>> B.x = 2
          >>> print(A.x, B.x, C.x)
          f47d8afc4ecbe93ca0a927e6f3d9c6db
          # locked
          >>> A.x += 1
          >>> print(A.x, B.x, C.x)
          23de34fa034ef4a8974f5f7cf5a23af2
          # locked
          >>> obj = C()
          >>> obj.y = 1
          >>> C.y == obj.y
          bcaec1dbeeb448da154a35169f563216
          # locked
          >>> A.y = obj.y
          >>> print(A.y, B.y, C.y, obj.y)
          e052c3cfb9a685bdd70e85cbe3a99593
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': False,
      'type': 'wwpp'
    }
  ]
}
