---
title: Winning Team
date: 2017-10-31
label: readme
---

# Requirements

Python 3

numpy

	sudo apt install python-numpy

scipy

	sudo apt install python-scipy

# The Data

Source: https://cricsheet.org/

YAML format: https://cricsheet.org/format/

We have three different data sets: IPL, BBL, and T20 internationals.

# Input Features

Note: We won't use all the features. Some of them (like number of balls) are just to help compute the others.

average = total runs / total number of matches where player batted

strike rate = 100 x total runs / number of balls played

50s :: player, matches -> matches where player scored 50-99 runs

100s :: player, matches -> matches where player scored 100+ runs

## Bowlers

balls bowled :: player, balls -> balls bowled by player

runs given :: player, balls -> runs given by bowler

wickets taken :: player, balls -> wickets taken by player

average = number of runs given / number of wickets taken

strike rate = balls bowled / wickets

wickets in match :: player, match -> wickets

5Ws = player, matches -> 5-wicket hauls

3Ws = player, matches -> 3-wicket hauls

## Wishlist of features

Quality of opponents: opposition team or squad (with stats)

number of man of the match awards

# Report

## Stats

all batting features - all seasons - different training percentages - different classifiers - different feature selection algorithms - different number of features

batting combo - all configurations (like above)

bowling combo - all configurations (like above)

all features - per season - 0.70 training percentage - different classifiers - different feature selection algorithms - different number of features

one feature at a time - all seasons - different training percentages - different classifiers - different feature selection algorithms - different number of features

## Tables

Primal outnumbers the rest in the top 10%, etc.

One table shows (y = _, rest = r') vs accuracy

Sometimes, (#features = _, feature = _, rest = c) vs accuracy

Variables: feature types; all seasons vs per season; training percentages; classifiers; feature selection algorithms; number of features to select

feature type vs accuracy: feature types = _; all seasons; 0.7; primal; greedy; 22

all seasons or per season vs accuracy: feature type = all features; all seasons = 2-10; 0.7; primal; greedy; 22

percentage of data vs accuracy: feature type = all features; all seasons = 2-10; percentage = _; primal; greedy; 22

classifier vs accuracy: feature type = all features; all seasons = 2-10; 0.7; classifier = _; greedy; 22

feature selection algorithm vs accuracy: feature type = all features; all seasons = 2-10; 0.7; primalsvm; feature selection algorithm = _; number of features = _

finals vs league matches: feature type = all features; per season; 1 - 4/n; primalsvm; greedy; 22

other leagues: league = _; feature type = all features; all seasons; 0.7; classifier = _; greedy; 22

## Plots

TODO
