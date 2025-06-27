test = {
  'name': 'Problem 11',
  'points': 250,
  'suites': [
    {
      'cases': [
        {
          'answer': 'f79b68cb2aaac8cd4ab0e49b17347556',
          'choices': [
            r"""
            It is waterproof, so its health won't be reduced to 0 when it is
            placed in a Water Place
            """,
            r"""
            It is not waterproof, so its health will be reduced to 0 when it is
            placed in a Water Place
            """,
            'It throws water pellets instead of leaves'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How is a ScubaThrower different from a regular ThrowerAnt?'
        },
        {
          'answer': 'e6fb1e56c024811a098edae1ab707fba',
          'choices': [
            'name, is_waterproof, food_cost',
            'food_cost, action, damage',
            'is_waterproof, action',
            'name, nearest_bee, is_waterproof'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          Which inherited attributes and/or methods should ScubaThrower
          override?
          """
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing ScubaThrower parameters
          >>> scuba = ScubaThrower()
          >>> ScubaThrower.food_cost
          33619aeb86b1e8373de8f936435956ec
          # locked
          >>> scuba.health
          f8350ec306c6ded66ec5181d85e1da56
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': False,
      'setup': r"""
      >>> from ants import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing if ScubaThrower is waterproof
          >>> water = Water('Water')
          >>> ant = ScubaThrower()
          >>> water.add_insect(ant)
          >>> ant.place is water
          f36ee348506dce0a1c70d2d603d21c7f
          # locked
          >>> ant.health
          f8350ec306c6ded66ec5181d85e1da56
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Testing that ThrowerAnt is not waterproof
          >>> water = Water('Water')
          >>> ant = ThrowerAnt()
          >>> water.add_insect(ant)
          >>> ant.place is water
          283113db14c20c490d6afa7240f170f0
          # locked
          >>> ant.health
          ca4502ed3a7078da4262913fdd77223b
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Testing ScubaThrower on land
          >>> place1 = gamestate.places["tunnel_0_0"]
          >>> place2 = gamestate.places["tunnel_0_4"]
          >>> ant = ScubaThrower()
          >>> bee = Bee(3)
          >>> place1.add_insect(ant)
          >>> place2.add_insect(bee)
          >>> ant.action(gamestate)
          >>> bee.health  # ScubaThrower can throw on land
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Testing ScubaThrower in the water
          >>> water = Water("water")
          >>> water.entrance = gamestate.places["tunnel_0_1"]
          >>> target = gamestate.places["tunnel_0_4"]
          >>> ant = ScubaThrower()
          >>> bee = Bee(3)
          >>> water.add_insect(ant)
          >>> target.add_insect(bee)
          >>> ant.action(gamestate)
          >>> bee.health  # ScubaThrower can throw in water
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(beehive, ant_types(), layout, dimensions)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing ScubaThrower Inheritance from ThrowerAnt
          >>> def new_action(self, gamestate):
          ...     raise NotImplementedError()
          >>> def new_throw_at(self, target):
          ...     raise NotImplementedError()
          >>> ThrowerAnt.action = new_action
          >>> test_scuba = ScubaThrower()
          >>> try:
          ...     test_scuba.action(gamestate)
          ... except NotImplementedError:
          ...     print('inherits action!')
          inherits action!
          >>> ThrowerAnt.action = old_thrower_action
          >>> ThrowerAnt.throw_at = new_throw_at
          >>> test_scuba = ScubaThrower()
          >>> try:
          ...     test_scuba.throw_at(Bee(1))
          ... except NotImplementedError:
          ...     print('inherits throw_at!')
          inherits throw_at!
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(beehive, ant_types(), layout, dimensions)
      >>> old_thrower_action = ThrowerAnt.action
      >>> old_throw_at = ThrowerAnt.throw_at
      """,
      'teardown': r"""
      >>> ThrowerAnt.action = old_thrower_action
      >>> ThrowerAnt.throw_at = old_throw_at
      """,
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from ants import *
          >>> ScubaThrower.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
