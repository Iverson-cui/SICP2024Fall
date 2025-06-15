test = {
  'name': 'Question 1: Lists',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> s = [7//3, 5, [4, 0, 1], 2]
          >>> s[0]
          65a47bff60899a5892a104ca2a620277
          # locked
          >>> s[2]
          7d5da345d99674c9642874c9d97d7c65
          # locked
          >>> s[-1]
          65a47bff60899a5892a104ca2a620277
          # locked
          >>> len(s)
          0ad0b7f800723aae04d9fa8e47682d31
          # locked
          >>> 4 in s
          35553e4416e886d1b22912c1ad8a181f
          # locked
          >>> 4 in s[2]
          04758b8d8526f959d281e01decd75f23
          # locked
          >>> s + [3 + 2, 9]
          c381695f9da750245f89e9c2acfa9a72
          # locked
          >>> s[2] * 2
          ae7c94ba4d5dc8873f5d6c11fa402506
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> x = [1, 2, 3, 4]
          >>> x[1:3]
          9414cd397806e9d7ff6ef74e0aba56bf
          # locked
          >>> x[:2]
          310a651c107154c75485727955251038
          # locked
          >>> x[1:]
          9339bae1a72f991e9f4d4285a792964d
          # locked
          >>> x[-2:3]
          5e6c701b00a15b58c57a281be93e9f94
          # locked
          >>> x[-2:4]
          6e26e2875be00ab7ba962a099caf3c9e
          # locked
          >>> x[0:4:2]
          37033bdad4b6b246ef8a00c6ba1fc030
          # locked
          >>> x[::-1]
          bac009edaa596e6672a250aa0e287ca5
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
