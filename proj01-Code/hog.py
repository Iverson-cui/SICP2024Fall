"""Project 1: The Game of Hog."""

from dice import six_sided, make_test_dice
from math import floor, sqrt
import doctest

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

# ANSWER QUESTION 00


# compared with dice, roll_dice means roll a dice multiple times and return the sum value, while dice just means roll a dice once.
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.


    >>> roll_dice(1, make_test_dice(4, 6, 1))
    4
    >>> roll_dice(2, make_test_dice(4, 6, 1))
    10

    """
    # BEGIN PROBLEM 1

    assert num_rolls > 0, "Must roll at least once."
    total, has_one = 0, False
    for num in range(num_rolls):
        temp = dice()
        total += temp
        if temp == 1:
            has_one = True
    return 1 if has_one else total
    # END PROBLEM 1


def picky_piggy(opponent_score):
    """Return the points scored from rolling 0 dice accodring to Picky Piggy.

    opponent_score:  The total score of the other player.
    """
    # BEGIN PROBLEM 2
    assert opponent_score >= 0, "Opponent's score must be non-negative."
    ones = opponent_score % 10
    tens = (opponent_score // 10) % 10
    return 2 * abs(tens - ones) + 1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Return the points scored for the turn rolling NUM_ROLLS dices when the
    opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return picky_piggy(opponent_score)
    assert num_rolls > 0, "Must roll at least once."
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def swine_swap(score):
    """Return whether the players' scores will be swapped due to Swine Swap.

    score:           The total score of the current player.

    Hint: for this problem, you will find the math function sqrt useful.
    >>> sqrt(9)
    3.0
    >>> floor(sqrt(9))
    3
    >>> floor(sqrt(8))
    2
    """
    # BEGIN PROBLEM 4
    return score == floor(sqrt(score)) ** 2
    # END PROBLEM 4


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5) simulates a game in which both
    players always choose to roll 5.

    A strategy function, such as always_roll_5, takes the current player's
    score and the opponent's score, and returns the number of dice that the
    corresponding player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5

    # check score0, score1 and goal is non-negative integer
    assert (
        score0 >= 0 and score1 >= 0 and goal > 0
    ), "Scores must be non-negative integers."
    while score0 < goal and score1 < goal:
        if who == 0:
            # player 0's turn
            score0 += take_turn(strategy0(score0, score1), score1, dice)
            if swine_swap(score0):
                score0, score1 = score1, score0
        elif who == 1:
            # player 1's turn
            score1 += take_turn(strategy1(score1, score0), score0, dice)
            if swine_swap(score1):
                score0, score1 = score1, score0
        who = 1 - who  # Switch turns
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the oppononent's score.
    """
    return 5


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    return lambda score, opponent_score: n
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL_SCORE):
    """Return whether strategy always chooses the same number of dice to roll.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    diff = False
    num = strategy(0, 0)
    for score in range(goal):
        for opponent_score in range(goal):
            # if the strategy returns a different number of rolls
            if num != strategy(score, opponent_score):
                diff = True
                return (
                    not diff
                )  # return False if the strategy returns a different number of rolls
    return (
        not diff
    )  # return True if the strategy always returns the same number of rolls
    # END PROBLEM 7


# if original_function is dice, this means roll the dice trials_count times and return the average value.
# if original_function is roll_dice, this means roll the dice multiple times in one trials_count and return the average value of the outcomes. Each outcome is the sum of the multiple-time rolls.
def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8

    def averaged_function(*args):
        sum = 0
        for _ in range(trials_count):
            sum += original_function(*args)
        return sum / trials_count

    return averaged_function

    # END PROBLEM 8


# rolling a dice from 0 to 10 times, see how many roll times gives the highest average score.
def max_scoring_num_rolls(dice=six_sided, total_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_num_rolls = 0
    max_avg = 0
    for num_rolls in range(1, 11):
        avg = make_averaged(roll_dice, total_samples)(num_rolls, dice)
        if avg > max_avg:
            max_avg = avg
            max_num_rolls = num_rolls
    return max_num_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print("Max scoring num rolls for six-sided dice:", six_sided_max)

    print("always_roll(6) win rate:", average_win_rate(always_roll(6)))  # near 0.5
    print("catch_up win rate:", average_win_rate(catch_up))
    print("always_roll(3) win rate:", average_win_rate(always_roll(3)))
    print("always_roll(8) win rate:", average_win_rate(always_roll(8)))

    print("picky_strategy win rate:", average_win_rate(picky_strategy))
    print("swine_strategy win rate:", average_win_rate(swine_strategy))
    print("final_strategy win rate:", average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def picky_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least THRESHOLD points,
    and returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if picky_piggy(opponent_score) >= threshold:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


def swine_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice when this would gives the player at least
    THRESHOLD points in this turn. Otherwise, it returns NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    # roll 0 times get score picky_piggy(opponent_score)
    # swap if swine_swap(score+picky_piggy(opponent_score))
    # I can get (opponent_score - score) more. Compare it with threshold.
    if swine_swap(score + picky_piggy(opponent_score)):
        if opponent_score - score >= threshold:
            return 0
    return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    # If I'm ahead, I want to roll fewer dice to avoid losing points.
    # If I'm behind, I want to roll more dice to catch up.
    # Tools you have: max_scoring_num_rolls, which we use to see in common cases how many rolls should be made(in six-sided case, this number is 6); swine_strategy and picky_strategy needs to be used every turn to see if we can get a better score; the threashold is calculated by make_averaged, we pass in the max_scoring_num_rolls to see what is the average score of rolling that many times, and use it as the threashold.
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    threshold = make_averaged(roll_dice, 100)(6, six_sided)
    should_picky = picky_strategy(
        score,
        opponent_score,
        threshold=threshold,
        num_rolls=3,
    )
    should_swine = swine_strategy(
        score,
        opponent_score,
        threshold=threshold,
        num_rolls=3,
    )
    if should_picky == 0 or should_swine == 0:
        return 0
    return catch_up(score, opponent_score)  # Use catch_up strategy as default
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


if __name__ == "__main__":
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="Runs strategy experiments"
    )

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()


if __name__ == "__main__":
    doctest.run_docstring_examples(roll_dice, globals(), verbose=True)
