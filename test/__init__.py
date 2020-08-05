import unittest
from test_funcs_match import *

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from match import Match

class testMatch(unittest.TestCase):
    def test_info(self):
        test_match = Match('2018-02-17', 'Match Type', 'Team 1', 'Team 2', 'Winner',
                           'MVP', 'toss_winner', 'toss_decision', ['Umpire 1', 'Umpire 2'], 'Venue')
        test_match.add_umpire()
        self.assertTrue(date_works(test_match.date)) 
        self.assertTrue(type_works(test_match.type)) 
        self.assertTrue(team1_works(test_match.teams[0])) 
        self.assertTrue(team2_works(test_match.teams[1])) 
        self.assertTrue(winner_works(test_match.winner)) 
        self.assertTrue(mvp_works(test_match.mvp)) 
        self.assertTrue(toss_winner_works(test_match.toss_winner)) 
        self.assertTrue(toss_decision_works(test_match.toss_decision))
        self.assertTrue(umpire_works(test_match.umpires[0], len(test_match.all_my_umpires))) 
        self.assertTrue(venue_works(test_match.venue)) 

    def test_display(self):
        test_match = Match('2018-02-17', 'Match Type', 'Team 1', 'Team 2', 'Winner',
                           'MVP', 'toss_winner', 'toss_decision', ['Umpire 1', 'Umpire 2'], 'Venue')
        test_match.add_umpire()
        match_string = test_match
        match_string_2 = str(match_string)
        match_string_3 = match_string_2.splitlines()
        self.assertTrue(string_works(match_string_3))
if __name__ == '__main__':
    unittest.main()
