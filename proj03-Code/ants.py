"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""

    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []  # A list of Bees
        self.ant = None  # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # Only when a place is set as the exit of another place, it has entrance.
        # BEGIN PROBLEM 2
        if self.exit is not None:
            self.exit.entrance = self
        # END PROBLEM 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    next_id = 0  # Every insect gets a unique id number
    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 10
    is_waterproof = False  # Insects that are waterproof do not die in water
    # END PROBLEM 10

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place

        # assign a unique ID to every insect
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            # the place of the insect is set to None when its health reaches 0
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn."""

    def zero_health_callback(self):
        """Called when health reaches 0 or below."""

    def add_to(self, place):
        self.place = place

    # remove_from belongs to Insect class.
    # It is used to remove an insect from a place, which is input
    def remove_from(self, place):
        # set the place attribute of the insect to None
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return "{0}({1}, {2})".format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    buffed = False
    # ADD CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM Optional 1

    def __init__(self, health=1):
        super().__init__(health)

    @classmethod
    def construct(cls, gamestate):
        """Create an Ant for a given GameState, or return None if not possible."""
        if cls.food_cost > gamestate.food:
            print("Not enough food remains to place " + cls.__name__)
            return
        return cls()

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        # place has no ants
        if place.ant is None:
            place.ant = self
        # place already has an ant
        else:
            # BEGIN PROBLEM 8
            # if ant in the place is a container ant
            if place.ant.is_container and place.ant.can_contain(self):
                place.ant.store_ant(self)
            # if ant in the place is not a container ant
            elif self.is_container and self.can_contain(place.ant):
                self.store_ant(place.ant)
                place.ant = self
            else:
                assert False, "Two ants in {0}".format(place)
            # END PROBLEM 8
        Insect.add_to(self, place)

    def remove_from(self, place):
        # if the place contains itself
        if place.ant is self:
            # remove the ant attribute from place instance
            place.ant = None
        # if the place contains no ants
        elif place.ant is None:
            assert False, "{0} is not in {1}".format(self, place)
        # if the place contains a container ant
        else:
            place.ant.remove_ant(self)

        # No matter what, remove the place attribute from insect instance
        Insect.remove_from(self, place)

    def buff(self):
        """Double this ants's damage, if it has not already been buffed."""
        # BEGIN PROBLEM 12
        # will the damage *= 2 be kept when it does its action?
        if self.buffed:
            return
        self.damage *= 2
        self.buffed = True
        # END PROBLEM 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = "Harvester"
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 1
    food_cost = 2
    health = 1
    # END PROBLEM 1

    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN PROBLEM 1
        gamestate.food += 1
        # END PROBLEM 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = "Thrower"
    implemented = True
    damage = 1

    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 1
    food_cost = 3
    health = 1
    # END PROBLEM 1
    # BEGIN PROBLEM 4
    min_range = 0
    max_range = float("inf")  # No limit on range by default
    # END PROBLEM 4

    def nearest_bee(self):
        """Return the nearest Bee in a Place (that is not the hive) connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN PROBLEM 3 and 4

        # if there is bee at the current place
        place = self.place
        distance = 0
        while place is not None and not place.is_hive:
            if self.min_range <= distance <= self.max_range:
                if len(place.bees) > 0:
                    return random_bee(place.bees)
                # if not, recursively look for further places
                place = place.entrance
                distance += 1
            else:
                place = place.entrance
                distance += 1
                continue

        return None
        # END PROBLEM 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), (
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    )
    if bees:
        return random.choice(bees)


##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = "Short"
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 4
    implemented = True  # Change to True to view in the GUI
    min_range = 0
    max_range = 3  # Only throws at Bees at most 3 places away
    # END PROBLEM 4


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = "Long"
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 4
    implemented = True  # Change to True to view in the GUI
    min_range = 5  # Only throws at Bees at least 5 places away
    max_range = float("inf")  # No limit on range by default
    # END PROBLEM 4


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = "Fire"
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 5
    implemented = True  # Change to True to view in the GUI
    # health = 3

    # END PROBLEM 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN PROBLEM 5
        # get bees list before reducing health
        bee_lst = self.place.bees[:]

        # every time damage is caused, the list may change
        # so we need to trim the list each time damage is caused
        # damage
        for bee in bee_lst:
            bee.reduce_health(amount)
        # trim
        bee_lst = [bee for bee in bee_lst if bee.health > 0]
        if self.health - amount <= 0:
            # If the FireAnt has no health remaining, it causes extra damages
            # damage
            for bee in bee_lst:
                bee.reduce_health(self.damage)
        # trim
        self.place.bees = [
            remaining_bee for remaining_bee in bee_lst if remaining_bee.health > 0
        ]
        super().reduce_health(amount)

        # END PROBLEM 5


# BEGIN PROBLEM 6
class WallAnt(Ant):
    name = "Wall"
    food_cost = 4
    implemented = True  # Change to True to view in the GUI

    def __init__(self, health=4):
        """Create a WallAnt with a HEALTH quantity."""
        super().__init__(health)


# END PROBLEM 6


# BEGIN PROBLEM 7
# The HungryAnt Class
class HungryAnt(Ant):
    name = "Hungry"
    food_cost = 4
    implemented = True  # Change to True to view in the GUI
    chew_duration = 3  # The number of turns it takes to chew

    def __init__(self, health=1):
        """Create a HungryAnt with a HEALTH quantity."""
        super().__init__(health)
        self.chew_countdown = 0

    def action(self, gamestate):
        """A HungryAnt's action is to eat a Bee in its Place, if it has not
        already eaten one this turn.
        """
        if self.chew_countdown > 0:
            self.chew_countdown -= 1
            return

        # If there are bees in the place, eat one
        if self.place.bees:
            bee = random_bee(self.place.bees)
            if bee:
                bee.reduce_health(bee.health)
                self.chew_countdown = self.chew_duration  # Reset the countdown


# END PROBLEM 7


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    """

    is_container = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN PROBLEM 8
        if isinstance(other, Ant) and not other.is_container:
            if self.ant_contained is None:
                return True
        return False
        # END PROBLEM 8

    def store_ant(self, ant):
        # BEGIN PROBLEM 8
        self.ant_contained = ant
        # END PROBLEM 8

    # special method for container ants to remove the ant contained.
    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants
        if place.ant is self:
            # Container was removed. Contained ant should remain in the place
            place.ant = place.ant.ant_contained
            # remove the container ant from the place
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN PROBLEM 8
        self.ant_contained.action(gamestate) if self.ant_contained else None
        # END PROBLEM 8


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants."""

    name = "Bodyguard"
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 8
    implemented = True  # Change to True to view in the GUI

    def __init__(self, health=2):
        """Create a BodyguardAnt with a HEALTH quantity."""
        super().__init__(health)

    # END PROBLEM 8


# BEGIN PROBLEM 9
# The TankAnt class
class TankAnt(ContainerAnt):
    """TankAnt is a BodyguardAnt that can also attack."""

    name = "Tank"
    food_cost = 6
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 9
    implemented = True  # Change to True to view in the GUI

    def __init__(self, health=2):
        """Create a TankAnt with a HEALTH quantity."""
        super().__init__(health)

    def action(self, gamestate):
        """A TankAnt's action is to attack all Bees in its Place."""
        bee_lst = self.place.bees[:]
        for bee in bee_lst:
            bee.reduce_health(self.damage)
        self.place.bees = [bee for bee in bee_lst if bee.health > 0]
        super().action(gamestate)  # Call the action of the contained ant if any


# END PROBLEM 9


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN PROBLEM 10
        super().add_insect(insect)
        if not insect.is_waterproof:
            insect.reduce_health(insect.health)
        # END PROBLEM 10


# BEGIN PROBLEM 11
# The ScubaThrower class
class ScubaThrower(ThrowerAnt):
    """ScubaThrower is a ThrowerAnt that can throw leaves from water."""

    name = "Scuba"
    food_cost = 6
    is_waterproof = True
    # OVERRIDE CLASS ATTRIBUTES HERE

    implemented = True  # Change to True to view in the GUI

    def __init__(self, health=1):
        """Create a ScubaThrower with a HEALTH quantity."""
        super().__init__(health)


# END PROBLEM 11


# BEGIN PROBLEM 12
class QueenAnt(ScubaThrower):
    # END PROBLEM 12
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = "Queen"
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 12
    implemented = True  # Change to True to view in the GUI
    # END PROBLEM 12

    @classmethod
    def construct(cls, gamestate):
        """
        Returns a new instance of the Ant class if it is possible to construct, or
        returns None otherwise. Remember to call the construct() method of the superclass!
        """
        # BEGIN PROBLEM 12
        if gamestate.has_queen is False:
            gamestate.has_queen = True  # Set the has_queen flag to True
            return super().construct(gamestate)
        return None
        # END PROBLEM 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN PROBLEM 12
        super().action(gamestate)  # Call the action of the ScubaThrower
        # Double the damage of all ants in the tunnel
        place = self.place.exit
        # make sure place is correct
        while place is not None and not place.is_hive:
            # make sure ant is correct
            if place.ant is not None:
                place.ant.buff()
                if place.ant.is_container and place.ant.ant_contained:
                    place.ant.ant_contained.buff()
            place = place.exit
        # END PROBLEM 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN PROBLEM 12
        super().reduce_health(amount)
        if self.health <= 0:
            # If the QueenAnt has no health remaining, signal the end of the game
            ants_lose()
        # END PROBLEM 12

    # BEGIN PROBLEM 12
    def remove_from(self, place):
        return

    # END PROBLEM 12


###################
# Extra Challenge #
###################


class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = "Slow"
    food_cost = 4
    # BEGIN PROBLEM EC
    implemented = True  # Change to True to view in the GUI
    # END PROBLEM EC

    def throw_at(self, target):
        if target:
            target.slow(3)
            target.action = lambda gamestate: self.slow_action(target, gamestate)

            # Override the action method to slow the target

    def slow_action(self, target, gamestate):
        # if there is a target and the target is slowed
        if target and target.slow_duration > 0:
            # reduce the slow duration by 1
            target.slow_duration -= 1
            # if the target is a bee and gamestate.time is odd, it will not move this turn
            if isinstance(target, Bee) and gamestate.time % 2 == 1:
                return
            # if time is even, the bee will move
            elif isinstance(target, Bee):
                target.action(gamestate)  # Bee will move if not slowed
        else:
            target.action(gamestate)  # If not slowed, perform normal action
        return True


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = "Scary"
    food_cost = 6
    # BEGIN PROBLEM EC
    implemented = True  # Change to True to view in the GUI
    # END PROBLEM EC

    def throw_at(self, target):
        # BEGIN PROBLEM EC
        target.scare()  # Scare the target for 3 turns
        target.action = lambda gamestate: self.scare_action(
            target, gamestate
        )  # Override the action method
        # END PROBLEM EC

    def scare_action(self, target, gamestate):
        """Override the action method to make the Bee back away."""

        back_times = 0
        if target and target.slow_duration > 0 and gamestate.time % 2 == 1:
            # If the target is slowed, it will not move this turn
            return
        # If the target is a Bee, it will back away instead of moving forward
        if isinstance(target, Bee):
            # Move the Bee to its entrance (back away)
            if not target.place.entrance.is_hive and back_times < 2:
                target.move_to(target.place.entrance)
                back_times += 1
            elif back_times >= 2:
                # If it has backed away twice, it will perform its normal action
                target.action(gamestate)
        else:
            # If not a Bee, perform normal action
            target.action(gamestate)
        return True


#####################
# Optional Problems #
#####################


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.
    This class is optional.
    """

    name = "Ninja"
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 1
    implemented = False  # Change to True to view in the GUI
    # END PROBLEM Optional 1

    def action(self, gamestate):
        # BEGIN PROBLEM Optional 1
        "*** YOUR CODE HERE ***"
        # END PROBLEM Optional 1


class LaserAnt(ThrowerAnt):
    # This class is optional. Only one test is provided for this class.

    name = "Laser"
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 2
    implemented = False  # Change to True to view in the GUI
    # END PROBLEM Optional 2

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN PROBLEM Optional 2
        return {}
        # END PROBLEM Optional 2

    def calculate_damage(self, distance):
        # BEGIN PROBLEM Optional 2
        return 0
        # END PROBLEM Optional 2

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


########
# Bees #
########


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = "Bee"
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 10
    is_waterproof = True  # Bees are waterproof, so they do not die in water
    # END PROBLEM 10
    slow_duration = 0  # The number of turns this Bee will be slowed
    scared = False  # Whether this Bee has been scared before

    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN PROBLEM Optional 1
        return self.place.ant is not None
        # END PROBLEM Optional 1

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit

        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to(place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def slow(self, length):
        """Slow the bee for a further LENGTH turns."""
        # BEGIN PROBLEM EC
        self.slow_duration += length
        # END PROBLEM EC

    def scare(self):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        """
        # BEGIN PROBLEM EC
        if not self.scared:
            self.scared = True
        # END PROBLEM EC


class Wasp(Bee):
    """Class of Bee that has higher damage."""

    name = "Wasp"
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped."""

    name = "Boss"
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    is_hive = True

    def __init__(self, assault_plan):
        self.name = "Hive"
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)


###################
# Game Components #
###################


class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.has_queen = False  # Flag to check if the queen ant has been placed
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase("Ant Home Base")
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)

        register_place(self.beehive, False)
        create_places(self.base, register_place, self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self):  # Ask ants to take actions
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees):  # Ask bees to take actions
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0:  # Check if player won
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game."""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self)  # Bees invade from hive
                yield None  # After yielding, players have time to place ants
                self.ants_take_actions()
                self.time += 1
                yield None  # After yielding, wait for throw leaf animation to play, then ask bees to take action
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print("All bees are vanquished. You win!")
            yield True
        except AntsLoseException:
            print(
                "The bees reached homebase or the queen ant queen has perished. Please try again :("
            )
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        ant = ant_type.construct(self)
        if ant:
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = " (Food: {0}, Time: {1})".format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), "Cannot add {0} to AntHomeBase"
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes."""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception."""

    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""

    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""

    pass


###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water("water_{0}_{1}".format(tunnel, step), exit)
            else:
                exit = Place("tunnel_{0}_{1}".format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################


class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]
