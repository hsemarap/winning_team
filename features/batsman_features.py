#!/usr/bin/python3

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
        self.yaml_data = yaml_data

    def flatten_cricket_yaml_data(self, yaml_data):
        yaml_data['innings'] = flatten_list_of_dicts(yaml_data['innings'])
        yaml_data['innings']['1st innings']['deliveries'] = flatten_list_of_dicts(yaml_data['innings']['1st innings']['deliveries'])
        yaml_data['innings']['2nd innings']['deliveries'] = flatten_list_of_dicts(yaml_data['innings']['2nd innings']['deliveries'])
        return yaml_data

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
