"""Unit tests for Phase 1 of the Hog project in "Composing Programs".
   Project is described on
   https://inst.eecs.berkeley.edu//~cs61a/fa13/proj/hog/hog.html
   These tests also assume you write a free_bacon() function, which
   is not explicitly stated in the assignment, but the functionality
   is part of the assignment.
   Note that the requirements and starter code for this project
   are _not_ the same as in the version on cs61a.org.

How to run tests:
  In your hog project directory (parent of this directory), type:

  python3 -m unittest test/test_phase1.py

How to run the 'doctest' tests contained in hog.py:
  python3 -m doctest hog.py

Or, for more verbose output that shows all doctests being run:
  python3 -m doctest -v hog.py
"""

import unittest
from hog import *
from dice import make_test_dice

class TestPhase1(unittest.TestCase):

    def test_roll_dice(self):
        """roll_dice() should return sum of several 'rolls' of dice"""
        test_dice = make_test_dice(6, 5, 2, 3, 4, 5, 6, 6, 6, 6)
        self.assertEqual(6, roll_dice(1, dice=test_dice))
        self.assertEqual(7, roll_dice(2, dice=test_dice))
        self.assertEqual(12, roll_dice(3, dice=test_dice))
        self.assertEqual(24, roll_dice(4, dice=test_dice))
        self.assertEqual(49, roll_dice(10, dice=test_dice))

    def test_roll_dice_with_one(self):
        """Test roll_dice() when a 1 appears on at least one die"""
        test_dice = make_test_dice(1, 5, 1, 3, 1, 2, 3, 4, 5, 6)
        self.assertEqual(1, roll_dice(1, dice=test_dice))
        self.assertEqual(1, roll_dice(3, dice=test_dice))
        self.assertEqual(1, roll_dice(5, dice=test_dice))
        self.assertEqual(1, roll_dice(10, dice=test_dice))

    def test_free_bacon(self):
        """free bacon should give a score 1 + max digit in opponent score"""
        for score in range(0,10):
            expect = score+1
            self.assertEqual(expect, free_bacon(score),
                             f"free_bacon({score}) should be {expect}")
        self.assertEqual(2, free_bacon(10))
        self.assertEqual(2, free_bacon(11))
        self.assertEqual(3, free_bacon(12))
        self.assertEqual(3, free_bacon(21))
        self.assertEqual(3, free_bacon(22))
        self.assertEqual(6, free_bacon(54))
        self.assertEqual(6, free_bacon(25))
        self.assertEqual(6, free_bacon(50))
        self.assertEqual(10, free_bacon(39))
        self.assertEqual(10, free_bacon(98))
        self.assertEqual(10, free_bacon(90))

    def test_take_turn(self):
        """take a turn using different opponent scores and dice"""
        FACE_VALUE = 4
        test_dice = make_test_dice(FACE_VALUE) # always rolls same value
        # test the free bacon case
        self.assertEqual(10, take_turn(0, 29, dice=test_dice))
        self.assertEqual(8, take_turn(0, 75, dice=test_dice))
        self.assertEqual(1, take_turn(0, 0, dice=test_dice))
        # for rolls > 0 opponent score should be irrelevant
        self.assertEqual(FACE_VALUE, take_turn(1, 0, dice=test_dice))
        self.assertEqual(3*FACE_VALUE, take_turn(3, 0, dice=test_dice))
        self.assertEqual(3*FACE_VALUE, take_turn(3, 23, dice=test_dice))
        self.assertEqual(10*FACE_VALUE, take_turn(10, 23, dice=test_dice))
        # this case always gets a score of 1
        test_dice = make_test_dice(1, 1, 1, 1, 1)
        self.assertEqual(1, take_turn(1, 10, dice=test_dice))
        self.assertEqual(1, take_turn(2, 10, dice=test_dice))
        self.assertEqual(1, take_turn(3, 10, dice=test_dice))
        self.assertEqual(1, take_turn(9, 10, dice=test_dice))
        self.assertEqual(1, take_turn(10, 10, dice=test_dice))
        # a test die with 2 values to verify student code uses it
        FACE1 = 2
        FACE2 = 5
        test_dice = make_test_dice(FACE1, FACE2)
        self.assertEqual(FACE1, take_turn(1, 10, dice=test_dice))
        self.assertEqual(FACE2, take_turn(1, 10, dice=test_dice))
        self.assertEqual(FACE1+FACE2, take_turn(2, 10, dice=test_dice))
        self.assertEqual(2*FACE1+FACE2, take_turn(3, 10, dice=test_dice))
