#!/usr/bin/python3

import pprint
from itertools import chain, filterfalse, islice, repeat, tee
from collections import defaultdict

default_strike_rate = 100
# TODO: Change this to the actual average.
default_average = 10
default_bowling_economy = 9.0
default_bowling_strike_rate = 60.0

average_features_fn = lambda x, xs: x.get_features(Match.team_averages, xs)
strike_rate_features_fn = lambda x, xs: x.get_features(Match.team_strike_rates, xs)
bowling_economy_features_fn = lambda x, xs: x.get_features(Match.team_bowling_economies, xs)

bowler_dismissals = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled']

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

def get_player_stats_dict(matches):
    """Return a dict of all player stats over matches."""
    stats_dict = defaultdict(lambda: {'total runs': 0,
                                      'total balls': 0,
                                      'batsman matches played': 0,
                                      'bowler matches played': 0,
                                      'bowler balls': 0,
                                      'total runs given': 0,
                                      'total wickets': 0,
                                      })
    for match in matches:
        match_batsmen = {}
        match_bowlers = {}
        for ix, ball in match.balls():
            batsman = ball['batsman']
            stats_dict[batsman]['total runs'] += ball['runs']['batsman']
            stats_dict[batsman]['total balls'] += 1
            match_batsmen[batsman] = True

            bowler = ball['bowler']
            match_bowlers[bowler] = True
            stats_dict[bowler]['total runs given'] += ball['runs']['total']
            stats_dict[bowler]['bowler balls'] += 1

            if 'wicket' in ball and ball['wicket']['kind'] in bowler_dismissals:
                stats_dict[bowler]['total wickets'] += 1

        for batsman in match_batsmen:
            stats_dict[batsman]['batsman matches played'] += 1
        for bowler in match_bowlers:
            stats_dict[bowler]['bowler matches played'] += 1
    return stats_dict

def batsman_num_balls(match, player):
    total = 0
    for ball_num, ball in match.balls():
        if ball['batsman'] == player:
            # TODO: Check for extras
            total += 1

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

    def print_past_stats(self, stats_dict):
        team1 = self.get_first_batting_side_players()
        team2 = self.get_second_batting_side_players()
        for player in team1:
            print(player, batsman_total_over_matches(stats_dict, player))
        for player in team2:
            print(player, batsman_total_over_matches(stats_dict, player))

    def team_strike_rates(self, stats_dict, team):
        """Strike rates for all players in team using stats_dict.
        """
        strike_rates = [batsman_overall_strike_rate(stats_dict, player) for player in team]
        strike_rates = list(islice(chain(strike_rates, repeat(default_strike_rate)), 11))
        return strike_rates

    def team_averages(self, stats_dict, team):
        """Averages for all players in team using stats_dict.
        """
        averages = [batsman_average(stats_dict, player) for player in team]
        averages = list(islice(chain(averages, repeat(default_average)), 11))
        return averages

    def team_bowling_economies(self, stats_dict, team):
        """Bowling economies for all players in team using stats_dict.
        """
        economies = [bowler_economy(stats_dict, player) for player in team]
        economies = list(islice(chain(economies, repeat(default_bowling_economy)), 11))
        return economies

    def get_features(self, features_fn, past_matches):
        """Return features usable as a training data point.

        For now, return 11 players on the first-batting side, 11 players on
        the bowling side, and match outcome.

        features_fn must take a match, stats_dict, and team and return a list
        of features for the team.

        """
        stats_dict = get_player_stats_dict(past_matches)
        team1 = self.get_first_batting_side_players()
        team2 = self.get_second_batting_side_players()
        self.print_match_info()
        self.print_past_stats(stats_dict)

        result = []
        team1_features = features_fn(self, stats_dict, team1)
        team2_features = features_fn(self, stats_dict, team2)

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
        return default_strike_rate
    else:
        return 100 * total / balls

def batsman_total_over_matches(stats_dict, player):
    return stats_dict[player]['total runs']

def batsman_num_balls_over_matches(stats_dict, player):
    return stats_dict[player]['total balls']

def batsman_num_matches(stats_dict, player):
    return stats_dict[player]['batsman matches played']

def bowler_num_matches(stats_dict, player):
    return stats_dict[player]['bowler matches played']

def bowler_num_balls(stats_dict, player):
    return stats_dict[player]['bowler balls']

def bowler_num_overs(stats_dict, player):
    return bowler_num_balls(stats_dict, player) // 6

def bowler_total_runs_given(stats_dict, player):
    return stats_dict[player]['total runs given']

def bowler_total_wickets(stats_dict, player):
    return stats_dict[player]['total wickets']

def batsman_overall_strike_rate(stats_dict, player):
    balls = batsman_num_balls_over_matches(stats_dict, player)
    if balls == 0:
        return default_strike_rate
    else:
        return 100 * batsman_total_over_matches(stats_dict, player) / balls

def batsman_average(stats_dict, player):
    num_matches = batsman_num_matches(stats_dict, player)
    if num_matches == 0:
        return default_average
    else:
        return batsman_total_over_matches(stats_dict, player) / num_matches

def bowler_economy(stats_dict, player):
    num_overs = bowler_num_overs(stats_dict, player)
    if num_overs == 0:
        return default_bowling_economy
    else:
        return bowler_total_runs_given(stats_dict, player) / num_overs

def bowler_strike_rate(stats_dict, player):
    num_balls = bowler_num_balls(stats_dict, player)
    num_wickets = bowler_total_wickets(stats_dict, player)
    if num_wickets == 0:
        return default_bowling_strike_rate
    else:
        return num_balls / num_wickets
