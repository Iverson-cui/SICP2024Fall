test = {
  'name': 'Problem 1',
  'points': 150,
  'suites': [
    {
      'cases': [
        {
          'answer': 'f7a65f09cc67de4b8109eef6df7a2c6e',
          'choices': [
            r"""
            Placing an ant into the colony will decrease the colony's total
            available food by that ant's food_cost
            """,
            r"""
            Each turn, each Ant in the colony eats food_cost food from the
            colony's total available food
            """,
            r"""
            Each turn, each Ant in the colony adds food_cost food to the
            colony's total available food
            """
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the purpose of the food_cost attribute?'
        },
        {
          'answer': '5424eab8d379dec29a1497a53defff3d',
          'choices': [
            'class, all Ants of the same subclass cost the same to place',
            'class, all Ants cost the same to place no matter what type of Ant it is',
            'instance, the food_cost of an Ant depends on the location it is placed',
            'instance, the food_cost of an Ant is randomized upon initialization'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What type of attribute is food_cost?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> Ant.food_cost
          ca4502ed3a7078da4262913fdd77223b
          # locked
          >>> HarvesterAnt.food_cost
          62f5becf14884ba4e68499843298094e
          # locked
          >>> ThrowerAnt.food_cost
          93a6f393519cdb7e80c716e7c2009036
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Testing HarvesterAnt action
          >>> # Create a test layout where the colony is a single row with 9 tiles
          >>> beehive = Hive(make_test_assault_plan())
          >>> gamestate = GameState(beehive, ant_types(), dry_layout, (1, 9))
          >>> #
          >>> gamestate.food = 4
          >>> harvester = HarvesterAnt()
          >>> # Note that initializing an Ant here doesn't cost food, only
          >>> # deploying an Ant in the game simulation does
          >>> #
          >>> gamestate.food
          03021ab33d8138d65d20e0e29a63e2f7
          # locked
          >>> harvester.action(gamestate)
          >>> gamestate.food
          fa2e78b5c10970c5fe1c84fae30061ed
          # locked
          >>> harvester.action(gamestate)
          >>> gamestate.food
          33619aeb86b1e8373de8f936435956ec
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> HarvesterAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> from ants_plans import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
