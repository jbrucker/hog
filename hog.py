"""The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. 
    
    Return the sum of the outcomes unless any of the outcomes is 1. 
    In that case, return 1.
    Your implementation should always roll the dice *exactly* num_rolls times.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    sum_dice = 0
    # Can't early return from the loop when a 1 is encountered,
    # so we need to keep track if any 1s.
    got_one = False
    for roll in range(0, num_rolls):
        value = dice()
        got_one = got_one or value == 1
        sum_dice += value
    # stupid rule
    return 1 if got_one else sum_dice


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < GOAL_SCORE, 'The game should be over.'
    assert score >= 0, 'Negative score is not allowed.'

    max_digit = 0
    while score > 0:
        max_digit = max(max_digit, score % 10)
        score = score//10
    return max_digit + 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < GOAL_SCORE, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return free_bacon(opponent_score)
    return roll_dice(num_rolls, dice=dice)
    # END PROBLEM 3

# Playing a game

def select_dice(player_score, opponent_score):
    """Select six-sided dice unless the sum of player_score and opponent_score 
    is a multiple of 7, in which case select four-sided dice (Hog wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
    if (player_score + opponent_score)%7 == 0:
        return four_sided
    return six_sided

def swine_swap(score0, score1):
    """Return True if player's should exchange scores."""
    return score0 == 2*score1 or score1 == 2*score0


def other(player):
    """Return the other player, for a player numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def next_player(player: int, player_score: int, opponent_score: int):
    """Return the id of the next player who should take a turn.
    This method is not part of the ComposingPrograms hog starter code.
    """
    return other(player)


def play(strategy0, strategy1, goal=GOAL_SCORE, score0=0, score1=0):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    goal:       The game ends and someone wins when this score is reached.
    # These two params are in the 2020 version but not the ComposingPrograms version.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    """
    # Use a list so we can use the same code for both players' turns.
    # Using parallel arrays is not a good design, though.
    score = [score0, score1]
    strategy = [strategy0, strategy1]
    # the current player
    player = 0
    while score[0] < goal and score[1] < goal:
        opponent = other(player)
        num_dice = strategy[player](score[player], score[opponent])
        dice = select_dice(score[player], score[opponent])
        score_this_turn = take_turn(num_dice, score[opponent], dice)
        score[player] += score_this_turn
        if swine_swap(score[player], score[opponent]):
            score = [score[1], score[0]]
        player = next_player(player, score[player], score[opponent])
    # game over.

    return score[0], score[1]


#######################
# Phase 2: Strategies #
#######################

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(function, num_trials=1000):
    """Return a function that returns the average value of FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def average(*args):
        sum = 0.0
        for trial in range(num_trials):
            sum += function(*args)
        return sum/num_trials if num_trials > 0 else 0.0
    return average

    
    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(BASELINE_NUM_ROLLS)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    # this line is not in the 2013 starter code
    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, cutoff=BACON_MARGIN, num_rolls=BASELINE_NUM_ROLLS):
    """This strategy rolls 0 dice if that gives at least cutoff points, 
    and rolls num_rolls otherwise.
    """
    # BEGIN PROBLEM 10
    return 6  # Replace this statement
    # END PROBLEM 10

# This function is NOT in the 2020 version.
def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """
    "*** YOUR CODE HERE ***"
    return 5 # Replace this statement


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    return 6  # Replace this statement


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
