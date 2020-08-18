# War -- the simple card game

[War](https://bicyclecards.com/how-to-play/war/) is about as simple a game as there is. Players throw cards and the high card wins. In  case of a tie, players throw three cards face-down and once face-up. Again, high card wins. There is no strategy.

## What is this

This is a bare-bones implementation in Python3. I was surprised by some of the results, so I switched to the suposedly [higher-quality](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html) [random generator in numpy](https://numpy.org/doc/1.19/reference/random/generator.html). The goal was to see how long a game should be, but there was a bit of a surprise in the results. Note that games were capped at 5,000 turns to avoid infinite loops. The results were the same at a 10,000 turn cap. All rounds were 10,000 games long.

## Strategies

The difference in these trials is in what the players do when picking up their cards. This isn't an explicit part of the game, but if there are two cards on the table, they will be picked up in _some_ order, even if unintentionally. When playing in real life, I've never thought about the pick-up order, but a machine implementation needed to do something with the cards. This all came about because I wasn't happy with the runtime performance of shuffling the cards so I tried sorting. The median turn counts dropped, and here we are.

The `random` strategy shuffles the cards when picking up. `sort` orders the cards from low-to-high, `revsort` orders from high-to-low.

## Results and Interpretations

### standard

4 suits of 13

* Sorting (low-to-high) is better than the random strategy. It results in the shortest games, so long as your opponent is not doing the same.
* Reverse-sorting (high-to-low) is no better than sorting (low-to-high) in a head-to-head game. However, it is better against the "random" strategy. The risk in choosing this strategy is that your opponent may make the same choice, resulting in infinitely long games.
* If either player chooses a sorting strategy, the game will be much shorter. If the players choose the same strategy, the game will be longer.
* If both players reverse-sort, the game often goes on forever. The "cap" for the game was 5,000 turns, but the results were the same even if the cap was pushed to 10,000 turns. This is because aces will float to the top when there is one card left.
* If both players randomly sort their picked-up cards, games will be significantly longer than if either player uses a consistent pick-up strategy.

| Player A   | Player B   |   Freq (kHz) |   Turns (median) |   Turns (90th) |   Turns (95th) |   Turns (99th) |   Turns (max) |   "A" Win Rate |   Tie Rate |
|:-----------|:-----------|-------------:|-----------------:|---------------:|---------------:|---------------:|--------------:|---------------:|-----------:|
| random     | random     |        0.530 |             1182 |           2120 |           2237 |           2331 |          2354 |          50.3% |       0.0% |
| random     | sort       |        2.978 |              530 |            948 |           1000 |           1042 |          1052 |          43.5% |       0.0% |
| random     | revsort    |        1.200 |              790 |           1416 |           1495 |           1557 |          1573 |          34.2% |       0.0% |
| sort       | random     |        3.132 |              432 |            771 |            814 |            848 |           856 |          55.8% |       0.0% |
| sort       | sort       |       10.485 |             2503 |           4501 |           4750 |           4950 |          5000 |          48.8% |       0.9% |
| sort       | revsort    |        7.531 |              496 |            886 |            934 |            973 |           983 |          50.0% |       0.0% |
| revsort    | random     |        1.107 |              750 |           1344 |           1418 |           1477 |          1492 |          67.1% |       0.0% |
| revsort    | sort       |        7.239 |              410 |            731 |            771 |            803 |           811 |          50.7% |       0.0% |
| revsort    | revsort    |        0.252 |             2504 |           4501 |           4750 |           4950 |          5000 |           2.1% |      96.0% |

## Alternate Decks

### extra-lowcard

53 cards, 4 suits of 13 plus an extra "2"

Adding another low card should result in one player's hand always being out-of-sync with the other's -- one will have a period of 26, the other 27. Unless a war occurs with fewer than 4 cards in someone's deck, Player "A" will always have an even number of cards, Player "B" will always be odd. Despite being out-of-phase, the results here are consistent with the standard 52-card deck.

| Player A   | Player B   |   Freq. (kHz) |   Turns (median) |   Turns (90th) |   Turns (95th) |   Turns (99th) |   Turns (max) |   "A" Win Rate |   Tie Rate |
|:-----------|:-----------|--------------:|-----------------:|---------------:|---------------:|---------------:|--------------:|---------------:|-----------:|
| random     | random     |         0.598 |             1520 |           2731 |           2883 |           3004 |          3034 |          49.4% |       0.0% |
| random     | sort       |         3.106 |              458 |            816 |            861 |            897 |           906 |          42.7% |       0.0% |
| random     | revsort    |         1.125 |              858 |           1537 |           1622 |           1690 |          1707 |          33.0% |       0.0% |
| sort       | random     |         2.976 |              410 |            731 |            771 |            803 |           811 |          55.3% |       0.0% |
| sort       | sort       |         8.983 |             2505 |           4501 |           4750 |           4950 |          5000 |          48.5% |       0.9% |
| sort       | revsort    |         6.034 |              415 |            741 |            781 |            814 |           822 |          48.6% |       0.0% |
| revsort    | random     |         1.179 |              798 |           1428 |           1506 |           1569 |          1585 |          64.9% |       0.0% |
| revsort    | sort       |         7.132 |              407 |            725 |            764 |            796 |           804 |          49.0% |       0.0% |
| revsort    | revsort    |         0.267 |             2503 |           4501 |           4750 |           4950 |          5000 |           2.8% |      93.7% |

### collision-free

52 cards, one suit

Because there are no "war" events, the owner of the highest card in the deck cannot lose. It may take a while, but that lucky player must win. This is the equivalent of playing with a standard deck, but specifying suit precedence (spades > hearts > clubs > diamonds) in addition to value precedence.

| Player A   | Player B   |   Freq. (kHz) |   Turns (median) |   Turns (90th) |   Turns (95th) |   Turns (99th) |   Turns (max) |   "A" Win Rate |   Tie Rate |
|:-----------|:-----------|--------------:|-----------------:|---------------:|---------------:|---------------:|--------------:|---------------:|-----------:|
| random     | random     |         0.305 |             2520 |           4504 |           4752 |           4950 |          5000 |          50.1% |       0.0% |
| random     | sort       |         0.833 |             1293 |           2307 |           2433 |           2535 |          2560 |          49.9% |       0.0% |
| random     | revsort    |         0.341 |             1741 |           3097 |           3266 |           3402 |          3436 |          50.2% |       0.0% |
| sort       | random     |         0.758 |             1440 |           2571 |           2713 |           2826 |          2854 |          50.5% |       0.0% |
| sort       | sort       |        16.494 |              142 |            235 |            246 |            256 |           258 |          50.0% |       0.0% |
| sort       | revsort    |         2.764 |              830 |           1473 |           1554 |           1618 |          1634 |          50.8% |       0.0% |
| revsort    | random     |         0.354 |             1653 |           2935 |           3096 |           3224 |          3256 |          50.1% |       0.0% |
| revsort    | sort       |         2.721 |              825 |           1464 |           1544 |           1608 |          1624 |          50.0% |       0.0% |
| revsort    | revsort    |         0.233 |             5000 |           5000 |           5000 |           5000 |          5000 |           0.0% |     100.0% |

### two-suits

2 suits of 26 cards

With only two suits, wars should occur only half as often as with the standard deck. The value of a sorting strategy is diminished as compared to the standard deck. This is the equivalent of playing with a standard deck, but specifying color precedence (e.g. red > black) in addition to value precedence.

| Player A   | Player B   |   Freq. (kHz) |   Turns (median) |   Turns (90th) |   Turns (95th) |   Turns (99th) |   Turns (max) |   "A" Win Rate |   Tie Rate |
|:-----------|:-----------|--------------:|-----------------:|---------------:|---------------:|---------------:|--------------:|---------------:|-----------:|
| random     | random     |         0.366 |             2106 |           3767 |           3974 |           4140 |          4182 |          50.3% |       0.0% |
| random     | sort       |         1.787 |              639 |           1139 |           1202 |           1252 |          1264 |          47.1% |       0.0% |
| random     | revsort    |         0.651 |             2122 |           3796 |           4005 |           4172 |          4214 |          40.4% |       0.0% |
| sort       | random     |         1.730 |              968 |           1731 |           1827 |           1903 |          1922 |          52.1% |       0.0% |
| sort       | sort       |        16.929 |              110 |            185 |            195 |            202 |           204 |          48.8% |       0.0% |
| sort       | revsort    |         6.048 |              545 |            970 |           1023 |           1065 |          1076 |          54.3% |       0.0% |
| revsort    | random     |         0.689 |             1420 |           2541 |           2681 |           2793 |          2821 |          59.4% |       0.0% |
| revsort    | sort       |         6.116 |              570 |           1015 |           1070 |           1115 |          1126 |          45.0% |       0.0% |
| revsort    | revsort    |         0.236 |             2506 |           4501 |           4751 |           4950 |          5000 |           0.2% |      99.6% |

### eight-suits

8 suits of 6 cards

Having additional suits increases the chance of a war. Therefore the games are shorter. The power of sorting (or reverse-sorting) appears to be somewhat exaggerated, but is similar to the standard deck. Note that this deck is only 48 cards, which also reduces the turn count.

| Player A   | Player B   |   Freq. (kHz) |   Turns (median) |   Turns (90th) |   Turns (95th) |   Turns (99th) |   Turns (max) |   "A" Win Rate |   Tie Rate |
|:-----------|:-----------|--------------:|-----------------:|---------------:|---------------:|---------------:|--------------:|---------------:|-----------:|
| random     | random     |         1.750 |              452 |            810 |            855 |            891 |           900 |          50.0% |       0.0% |
| random     | sort       |         5.475 |              206 |            369 |            390 |            406 |           410 |          45.3% |       0.0% |
| random     | revsort    |         2.781 |              244 |            438 |            463 |            482 |           487 |          28.6% |       0.0% |
| sort       | random     |         5.542 |              230 |            412 |            434 |            452 |           457 |          54.3% |       0.0% |
| sort       | sort       |         9.850 |             2502 |           4500 |           4750 |           4950 |          5000 |          49.4% |       0.8% |
| sort       | revsort    |         9.665 |              308 |            552 |            582 |            607 |           613 |          35.4% |       0.0% |
| revsort    | random     |         2.820 |              327 |            586 |            619 |            645 |           651 |          71.0% |       0.0% |
| revsort    | sort       |         9.882 |              224 |            401 |            423 |            441 |           445 |          65.1% |       0.0% |
| revsort    | revsort    |         0.291 |             2502 |           4500 |           4750 |           4950 |          5000 |          10.2% |      79.2% |
