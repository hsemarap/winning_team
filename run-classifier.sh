#!/bin/bash

# ./features/extract_features.py

PYTHONPATH=`pwd`:`pwd`/features:$PYTHONPATH
export PYTHONPATH

python3 -m unittest features.batsman_features_test features.extract_features_test
# python3 -m unittest features.batsman_features_test.TestBatsmenFeatures.test_team_bowling_average_plus_strike_rate_plus_economy
