#!/bin/bash

./features/extract_features.py

PYTHONPATH=`pwd`:`pwd`/features:$PYTHONPATH
export PYTHONPATH

# python3 -m unittest features.batsman_features_test
# python3 -m unittest features.batsman_features_test.TestBatsmenFeatures.test_flatten_yaml_dict
