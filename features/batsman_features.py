#!/usr/bin/python3

import pprint
from itertools import chain

def flatten_list_of_dicts(dict_list):
    flat_dict = {}
    for d in dict_list:
        assert len(d.keys()) == 1
        for k,v in d.items():
            assert k not in flat_dict
            flat_dict[k] = v
    return flat_dict

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

    def balls(self):
        d1 = self.match_details['innings']['1st innings']['deliveries']
        d2 = self.match_details['innings']['2nd innings']['deliveries']
        return chain(d1.items(), d2.items())

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

def batsman_average(match, player):
    return batsman_total(match, player) / batsman_num_balls(match, player)
