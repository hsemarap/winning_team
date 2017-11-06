#!/usr/bin/python3

import pprint
from itertools import chain, filterfalse, islice, repeat, tee

def flatten_list_of_dicts(dict_list):
    flat_dict = {}
    for d in dict_list:
        assert len(d.keys()) == 1
        for k,v in d.items():
            # TODO: Can't assert this because 336024.yaml has 18.1 and 18.10,
            # which are represented as the same float.
            # assert k not in flat_dict
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
    def __init__(self, yaml_data, file_name):
        self.match_details = self.flatten_cricket_yaml_data(yaml_data)
        self.file_name = file_name

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

    def teams(self):
        return self.match_details['info']['teams']

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

    def print_match_info(self):
        print("\nMatch info:", self.file_name)
        print(self.teams())

    def print_past_stats(self, past_matches):
        team1 = self.get_first_batting_side_players()
        team2 = self.get_second_batting_side_players()
        for player in team1:
            print(player, batsman_total_over_matches(past_matches, player))
        for player in team2:
            print(player, batsman_total_over_matches(past_matches, player))

    def features(self, past_matches):
        """Return features usable as a training data point.

        For now, return 11 players on the first-batting side, 11 players on
        the bowling side, and match outcome.
        """
        team1 = self.get_first_batting_side_players()
        team2 = self.get_second_batting_side_players()
        self.print_match_info()
        self.print_past_stats(past_matches)

        result = []
        # TODO: Change this.
        default_feature_value = 0.0
        team1_features = [batsman_overall_strike_rate(past_matches, player) for player in team1]
        team1_features = list(islice(chain(team1_features, repeat(default_feature_value)), 11))
        team2_features = [batsman_overall_strike_rate(past_matches, player) for player in team2]
        team2_features = list(islice(chain(team2_features, repeat(default_feature_value)), 11))

        if self.first_batting_side_won():
            outcome = 1
        else:
            outcome = 0
        result = team1_features + team2_features + [outcome]
        assert len(result) == 23
        return result

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

def batsman_total_over_matches(matches, player):
    return sum([batsman_total(match, player) for match in matches])

def batsman_num_balls_over_matches(matches, player):
    return sum([batsman_num_balls(match, player) for match in matches])

def batsman_overall_strike_rate(matches, player):
    balls = batsman_num_balls_over_matches(matches, player)
    if balls == 0:
        return 0.0
    else:
        return 100 * batsman_total_over_matches(matches, player) / balls
