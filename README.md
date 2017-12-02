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
