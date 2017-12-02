#!/usr/bin/python3

from pprint import pprint
from itertools import chain, filterfalse, islice, repeat, tee
from collections import defaultdict

default_strike_rate = 100
# TODO: Change this to the actual average.
default_average = 10
default_bowling_economy = 9.0
default_bowling_strike_rate = 60.0
default_bowling_average = 60.0
default_win_rate = 50.0
default_net_run_rate = 0.0
default_average_plus_strike_rate = default_average + default_strike_rate

average_features_fn = lambda x, xs: x.get_features(Match.team_averages, xs)
strike_rate_features_fn = lambda x, xs: x.get_features(Match.team_strike_rates, xs)
bowling_economy_features_fn = lambda x, xs: x.get_features(Match.team_bowling_economies, xs)
bowling_strike_rate_features_fn = lambda x, xs: x.get_features(Match.team_bowling_strike_rates, xs)
team_win_rate_features_fn = lambda x, xs: x.get_team_features(Match.team_win_rate, xs)
team_net_run_rate_features_fn = lambda x, xs: x.get_team_features(Match.team_net_run_rate, xs)
batting_average_plus_strike_rate_features_fn = lambda x, xs: x.get_features(Match.team_batting_average_plus_strike_rate, xs)

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
                                      'bowler total runs given': 0,
                                      'bowler total wickets': 0,
                                      'wins': 0,
                                      'matches': 0,
                                      'team total runs made': 0,
                                      'team total runs given': 0,
                                      'team total balls batted': 0,
                                      'team total balls bowled': 0,
                                      })
    for match in matches:
        details = match.match_details
        team1 = match.first_batting_side()
        team2 = match.second_batting_side()
        stats_dict[team1]['matches'] += 1
        stats_dict[team2]['matches'] += 1
        if 'winner' in details['info']['outcome']:
            if details['info']['outcome']['winner'] == team1:
                stats_dict[team1]['wins'] += 1
            elif details['info']['outcome']['winner'] == team2:
                stats_dict[team2]['wins'] += 1

        for ix, ball in match.first_innings_balls():
            stats_dict[team1]['team total runs made'] += ball['runs']['total']
            stats_dict[team2]['team total runs given'] += ball['runs']['total']
            stats_dict[team1]['team total balls batted'] += 1
            stats_dict[team2]['team total balls bowled'] += 1

        for ix, ball in match.second_innings_balls():
            stats_dict[team2]['team total runs made'] += ball['runs']['total']
            stats_dict[team1]['team total runs given'] += ball['runs']['total']
            stats_dict[team2]['team total balls batted'] += 1
            stats_dict[team1]['team total balls bowled'] += 1

        match_batsmen = {}
        match_bowlers = {}
        for ix, ball in match.balls():
            batsman = ball['batsman']
            stats_dict[batsman]['total runs'] += ball['runs']['batsman']
            stats_dict[batsman]['total balls'] += 1
            match_batsmen[batsman] = True

            bowler = ball['bowler']
            match_bowlers[bowler] = True
            stats_dict[bowler]['bowler total runs given'] += ball['runs']['total']
            stats_dict[bowler]['bowler balls'] += 1

            if 'wicket' in ball and ball['wicket']['kind'] in bowler_dismissals:
                stats_dict[bowler]['bowler total wickets'] += 1

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

    def second_batting_side(self):
        rest = self.match_details['info']['teams'][:]
        rest.remove(self.first_batting_side())
        return rest[0]

    def first_batting_side_won(self):
        return self.winner() == self.first_batting_side()

    def print_match_info(self):
        print("\nMatch info:", self.file_name)
        print(self.teams())

    def print_past_stats(self, stats_dict):
        team1 = self.get_first_batting_side_players()
        team2 = self.get_second_batting_side_players()
        pprint(stats_dict[self.first_batting_side()])
        pprint(stats_dict[self.second_batting_side()])
        # for player in team1:
        #     print(player, stats_dict[player])
        # for player in team2:
        #     print(player, stats_dict[player])

    def team_strike_rates(self, stats_dict, team):
        """Strike rates for all players in team using stats_dict.
        """
        return self.team_stats_for_feature(stats_dict, team, batsman_overall_strike_rate, default_strike_rate)

    def team_averages(self, stats_dict, team):
        """Averages for all players in team using stats_dict.
        """
        return self.team_stats_for_feature(stats_dict, team, batsman_average, default_average)

    def team_batting_average_plus_strike_rate(self, stats_dict, team):
        """Average + strike rate for all players in team using stats_dict.
        """
        return self.team_stats_for_feature(stats_dict, team, batsman_average_plus_strike_rate, default_average_plus_strike_rate)

    def team_bowling_economies(self, stats_dict, team):
        """Bowling economies for all players in team using stats_dict.
        """
        return self.team_stats_for_feature(stats_dict, team, bowler_economy, default_bowling_economy)

    def team_bowling_strike_rates(self, stats_dict, team):
        """Bowling strike rates for all players in team using stats_dict."""
        return self.team_stats_for_feature(stats_dict, team, bowler_strike_rate, default_bowling_strike_rate)

    def team_stats_for_feature(self, stats_dict, team, stat_fn, default_value):
        """Get stat for all players in team."""
        features = [stat_fn(stats_dict, player) for player in team]
        features = list(islice(chain(features, repeat(default_value)), 11))
        return features

    def team_win_rate(self, stats_dict, team):
        """Get win rate for team (in a singleton list)."""
        num_wins = stats_dict[team]['wins']
        num_matches = stats_dict[team]['matches']
        if num_matches == 0:
            return [default_win_rate]
        else:
            return [num_wins / num_matches]

    def team_net_run_rate(self, stats_dict, team):
        """Get net run rate for team."""
        total_runs_made = stats_dict[team]['team total runs made']
        total_overs_batted = stats_dict[team]['team total balls batted'] // 6
        total_runs_given = stats_dict[team]['team total runs given']
        total_overs_bowled = stats_dict[team]['team total balls bowled'] // 6
        if total_overs_bowled == 0 or total_overs_batted == 0:
            return [default_net_run_rate]
        else:
            return [(total_runs_made / total_overs_batted) - (total_runs_given / total_overs_bowled)]

    def get_team_features(self, features_fn, past_matches):
        """Return features usable as a training data point."""
        stats_dict = get_player_stats_dict(past_matches)
        team1 = self.first_batting_side()
        team2 = self.second_batting_side()
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
        # assert len(result) == 23
        return result

    def get_features(self, features_fn, past_matches):
        """Return features usable as a training data point.

        For now, return 11 players on the first-batting side, 11 players on
        the bowling side, and match outcome.

        features_fn must take a match, stats_dict, and team and return a list
        of features for the team.

        """
        stats_dict = get_player_stats_dict(past_matches)
        team1_players = self.get_first_batting_side_players()
        team2_players = self.get_second_batting_side_players()
        self.print_match_info()
        self.print_past_stats(stats_dict)

        result = []
        team1_features = features_fn(self, stats_dict, team1_players)
        team2_features = features_fn(self, stats_dict, team2_players)

        if self.first_batting_side_won():
            outcome = 1
        else:
            outcome = 0
        result = team1_features + team2_features + [outcome]
        # assert len(result) == 23
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

# def batsman_strike_rate(match, player):
#     total = batsman_total(match, player)
#     balls = batsman_num_balls(match, player)
#     if balls == 0:
#         return default_strike_rate
#     else:
#         return 100 * total / balls

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
    return stats_dict[player]['bowler total runs given']

def bowler_total_wickets(stats_dict, player):
    return stats_dict[player]['bowler total wickets']

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

def batsman_average_plus_strike_rate(stats_dict, player):
    return batsman_average(stats_dict, player) + batsman_overall_strike_rate(stats_dict, player)

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

def bowler_average(stats_dict, player):
    num_wickets = bowler_total_wickets(stats_dict, player)
    num_runs = bowler_total_runs_given(stats_dict, player)
    if num_wickets == 0:
        return default_bowling_average
    else:
        return num_runs / num_wickets
