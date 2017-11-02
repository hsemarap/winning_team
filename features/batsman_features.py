#!/usr/bin/python3

def get_ball(match_data, innings, ball_index, ball_number):
    """Get ball (for test purposes).
    """
    # TODO: Replace 0.
    return match_data['innings'][0][innings]['deliveries'][ball_index][ball_number]

def runs_off_ball(player, ball):
    if player == ball['batsman']:
        return ball['runs']['batsman']
    else:
        return 0
