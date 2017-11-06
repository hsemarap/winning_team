#!/usr/bin/python3

import pprint
from itertools import chain, filterfalse

def flatten_list_of_dicts(dict_list):
    flat_dict = {}
    for d in dict_list:
        assert len(d.keys()) == 1
        for k,v in d.items():
            assert k not in flat_dict
            flat_dict[k] = v
    return flat_dict

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen.

    From https://docs.python.org/2/library/itertools.html"""
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

class Match:
    def __init__(self, yaml_data):
        self.match_details = self.flatten_cricket_yaml_data(yaml_data)

    def flatten_cricket_yaml_data(self, yaml_data):
        yaml_data['innings'] = flatten_list_of_dicts(yaml_data['innings'])
        yaml_data['innings']['1st innings']['deliveries'] = flatten_list_of_dicts(yaml_data['innings']['1st innings']['deliveries'])
        yaml_data['innings']['2nd innings']['deliveries'] = flatten_list_of_dicts(yaml_data['innings']['2nd innings']['deliveries'])
        return yaml_data

    def get_ball(self, innings, ball_number):
        """Get ball.
        """
        return self.match_details['innings'][innings]['deliveries'][ball_number]

    def first_innings_balls(self):
        d = self.match_details['innings']['1st innings']['deliveries']
        return d.items()

    def second_innings_balls(self):
        d = self.match_details['innings']['2nd innings']['deliveries']
        return d.items()

    def balls(self):
        return chain(self.first_innings_balls(), self.second_innings_balls())

    def get_players(self, batting_balls, bowling_balls):
        batsmen = [ball['batsman'] for ix, ball in batting_balls]
        non_strikers = [ball['non_striker'] for ix, ball in batting_balls]
        bowlers = [ball['bowler'] for ix, ball in bowling_balls]
        players = unique_everseen(
            chain(unique_everseen(batsmen),
                  unique_everseen(non_strikers),
                  unique_everseen(bowlers)))
        return players

    def get_first_batting_side_players(self):
        return self.get_players(self.first_innings_balls(), self.second_innings_balls())

    def get_second_batting_side_players(self):
        return self.get_players(self.second_innings_balls(), self.first_innings_balls())

    def winner(self):
        try:
            return self.match_details['info']['outcome']['winner']
        except:
            return None

    def first_batting_side(self):
        toss = self.match_details['info']['toss']
        teams = self.match_details['info']['teams']
        if toss['decision'] == 'bat':
            return toss['winner']
        else:
            # Hack because Python can't remove non-destructively.
            rest = teams[:]
            rest.remove(toss['winner'])
            return rest[0]

    def first_batting_side_won(self):
        return self.winner() == self.first_batting_side()

def runs_off_ball(player, ball):
    if player == ball['batsman']:
        return ball['runs']['batsman']
    else:
        return 0

def batsman_total(match, player):
    total = 0
    for ball_num, ball in match.balls():
        if ball['batsman'] == player:
            total += ball['runs']['batsman']
    return total

def batsman_num_balls(match, player):
    total = 0
    for ball_num, ball in match.balls():
        if ball['batsman'] == player:
            # TODO: Check for extras
            total += 1
    return total

def batsman_strike_rate(match, player):
    total = batsman_total(match, player)
    balls = batsman_num_balls(match, player)
    if balls == 0:
        return 0.0
    else:
        return 100 * total / balls

def batsman_overall_strike_rate(matches, player):
    total = sum([batsman_total(match, player) for match in matches])
    balls = sum([batsman_num_balls(match, player) for match in matches])
    if balls == 0:
        return 0.0
    else:
        return 100 * total / balls
