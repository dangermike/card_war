# War -- the simple card game

[War](https://bicyclecards.com/how-to-play/war/) is about as simple a game as there is. Players throw cards and the high card wins. In  case of a tie, players throw three cards face-down and once face-up. Again, high card wins. There is no strategy.

## What is this?

This is a bare-bones implementation in Python3. I was surprised by some of the results, so I switched to the suposedly [higher-quality](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html) [random generator in numpy](https://numpy.org/doc/1.19/reference/random/generator.html). The goal was to see how long a game should be, but there was a bit of a surprise in the results. Note that games were capped at 5,000 turns to avoid infinite loops. The results were the same at a 10,000 turn cap

## Strategies

The difference in these trials is in what the players do when picking up their cards. This isn't an explicit part of the game, but if there are two cards on the table, they will be picked up in _some_ order, even if unintentionally. When playing in real life, I've never thought about the pick-up order, but a machine implementation needed to do something with the cards. This all came about because I wasn't happy with the runtime performance of shuffling the cards so I tried sorting. The median turn counts dropped, and here we are.

The `random` strategy shuffles the cards when picking up. `sort` orders the cards from low-to-high, `revsort` orders from high-to-low.

## Results and Interpretations

| Player A | Player B | Median turns | A win rate | Hit cap |
| -------- | -------- | -----------: | ---------: | ------: |
| random   | random   |         1781 |     50.90% |       0 |
| random   | revsort  |          530 |     17.76% |       0 |
| sort     | random   |          656 |     68.09% |       0 |
| sort     | sort     |          160 |     49.63% |       0 |
| sort     | revsort  |          360 |     69.73% |       0 |
| revsort  | random   |          581 |     81.23% |       0 |
| revsort  | sort     |          347 |     29.84% |       0 |
| revsort  | revsort  |         2504 |      0.01% |    9996 |

* If both players reverse-sort, the game often goes on forever. The "cap" for the game was 5,000 turns, but the results were the same even if the cap was pushed to 10,000 turns. I think this has to do with how the game behaves when there is only one card.
* If both players randomly sort their picked-up cards, games will be significantly longer than if either player uses a consistent pick-up strategy.
* Sorting low-to-high is the most consistent winning strategy, though reverse-sorting is the most effective against a random opponent. I have not yet explained why sorting is so effective.
