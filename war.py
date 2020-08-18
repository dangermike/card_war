#!/usr/bin/env python3

from collections import deque
from datetime import datetime
from numpy.random import default_rng

import numpy

rng = default_rng()
deck = list(range(13)) * 4

GAME_COUNT = 10000
MAX_ROUNDS = 5000

cards = []
playerA = deque(maxlen=52)
playerB = deque(maxlen=52)

strategies = [
    ('random', rng.shuffle),
    ('sort', lambda x: x.sort()),
    ('revsort', lambda x: x.sort(reverse=True)),
]

for a_name, a_func in strategies:
    for b_name, b_func in strategies:
        games = []
        start = datetime.utcnow()
        wars = 0
        a_wins = 0
        ties = 0
        for _ in range(GAME_COUNT):
            rng.shuffle(deck)

            playerA.clear()
            playerB.clear()
            playerA.extend(deck[:26])
            playerB.extend(deck[26:])

            rounds = 0
            while len(playerA) > 0 and len(playerB) > 0 and rounds < MAX_ROUNDS:
                rounds += 1
                cards.clear()
                cardA = playerA.pop()
                cardB = playerB.pop()
                cards.append(cardA)
                cards.append(cardB)

                while cardA == cardB:
                    wars += 1
                    for _ in range(min(4, len(playerA))):
                        cardA = playerA.pop()
                        cards.append(cardA)

                    for _ in range(min(4, len(playerB))):
                        cardB = playerB.pop()
                        cards.append(cardB)

                if cardA > cardB:
                    a_func(cards)
                    playerA.extend(cards)
                else:
                    b_func(cards)
                    playerB.extend(cards)

            if rounds == MAX_ROUNDS:
                ties += 1
            elif len(playerA) > 0:
                a_wins += 1
            games.append(rounds)

        elapsed_ms = (datetime.utcnow() - start).total_seconds() * 1000
        _, bins = numpy.histogram(games, bins=100)
        print(
            "%s vs %s: Completed %d games at %0.3f kHz. Median turns: %d. %s won %0.3f%% of the time. %d hit max rounds (%d)."
            % (
                a_name,
                b_name,
                GAME_COUNT,
                GAME_COUNT / elapsed_ms,
                bins[50],
                a_name,
                100 * a_wins / GAME_COUNT,
                ties,
                MAX_ROUNDS,
            ))

        # print(bins)
        # print("min:    %d" % bins[0])
        # print("median: %d" % bins[25])
        # print("median: %d" % bins[50])
        # print("90th:   %d" % bins[90])
        # print("95th:   %d" % bins[95])
        # print("99th:   %d" % bins[99])
        # print("max:    %d" % bins[100])

# import matplotlib.pyplot as plt
# plt.hist(games, bins='sturges')
# plt.show()
