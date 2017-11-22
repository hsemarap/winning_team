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

## TODO: Features

Don't have separate dictionaries for each ball.

## Batsmen

runs off this ball :: player, ball -> runs scored by the player off this ball

ball played :: player, ball -> 1 if player played the ball, else 0

runs in match :: player, match -> runs scored by player in match

total number of matches played :: player, matches -> matches played by the player

total number of matches where player batted :: player, matches -> matches where the player batted

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

## Fielders

catches :: player, balls -> catches

run-outs :: player, balls -> run-outs

## Wishlist of features

Quality of opponents: opposition team or squad (with stats)

number of man of the match awards

# Output features

win/loss, net run rate

## Computing Features

Player stat :: matches -> stat

For example, a batsman's average after 10 matches will be total runs scored in those matches / number of matches where he batted.

# Wish list

Compute stats for a player including international T20 matches up to that date.

Maybe include player stats from ODI and Test matches too.


# To Do (PD)

Shuffle the input data before splitting train/testa

Add a function to generate the report for all combinations
