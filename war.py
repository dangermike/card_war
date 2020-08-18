#!/usr/bin/env python3

from datetime import datetime
from numpy.random import default_rng
from typing import Callable, List, Tuple

from deck import Deck
from result import CompileResults, GameResult, Outcome, RoundResult, print_results

Strategy = Callable[[List[int]], None]

# this is only used in pick-up strategies, not in shuffling the deck
rng = default_rng()

GAME_COUNT = 10000
MAX_ROUNDS = 5000

decks: List[Deck] = [
    Deck(
        'standard',
        '4 suits of 13',
        list(range(13)) * 4,
    ),
    Deck(
        'extra-lowcard',
        '53 cards, 4 suits of 13 plus an extra "2"',
        (list(range(13)) * 4) + [0],
    ),
    Deck(
        'collision-free',
        '52 cards, one suit',
        list(range(52)),
    ),
    Deck(
        'two-suits',
        '2 suits of 26 cards',
        list(range(26)) * 2,
    ),
    Deck(
        'eight-suits',
        '8 suits of 6 cards',
        list(range(6)) * 8,
    ),
]

strategies: List[Tuple[str, Strategy]] = [
    ('random', rng.shuffle),
    ('sort', lambda x: x.sort()),
    ('revsort', lambda x: x.sort(reverse=True)),
]


def play_game(
        deck: Deck,
        a_strategy: Strategy,
        b_strategy: Strategy,
) -> GameResult:
    playerA, playerB = deck.deal()

    rounds = 0
    wars = 0
    cards: List[int] = []

    # If the war ends in a tie and one player is out of cards, the game must
    # end. There is no fair resolution to this (rare) condition. Because of
    # that, it is possible that the winner will not have all the cards:
    # Some will be left on the table from the unresolved war.
    while len(playerA) > 0 and len(playerB) > 0 and rounds < MAX_ROUNDS:
        rounds += 1
        cards.clear()
        cardA = playerA.pop()
        cardB = playerB.pop()
        cards.append(cardA)
        cards.append(cardB)

        while cardA == cardB and len(playerA) > 0 and len(playerB) > 0:
            wars += 1
            for _ in range(min(4, len(playerA))):
                cardA = playerA.popleft()
                cards.append(cardA)

            for _ in range(min(4, len(playerB))):
                cardB = playerB.popleft()
                cards.append(cardB)

        if cardA > cardB:
            a_func(cards)
            playerA.extend(cards)
        elif cardB > cardA:
            b_func(cards)
            playerB.extend(cards)

    if rounds == MAX_ROUNDS:
        return GameResult(Outcome.Tie, wars, MAX_ROUNDS)
    elif len(playerA) > 0:
        return GameResult(Outcome.A, wars, rounds)
    else:
        return GameResult(Outcome.B, wars, rounds)


for deck in decks:
    results: List[RoundResult] = []

    for a_name, a_func in strategies:
        for b_name, b_func in strategies:
            start = datetime.utcnow()
            games = [
                play_game(deck, a_func, b_func) for _ in range(GAME_COUNT)
            ]

            results.append(
                CompileResults(
                    player_a=a_name,
                    player_b=b_name,
                    games=games,
                    elapsed=(datetime.utcnow() - start),
                ))

    print_results(deck, results)
