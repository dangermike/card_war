from datetime import timedelta
from enum import Enum
from tabulate import tabulate
from typing import List, NamedTuple

from deck import Deck

import numpy

HEADERS = [
    'Player A',
    'Player B',
    'Games',
    'Freq. (kHz)',
    'Turns (median)',
    'Turns (90th)',
    'Turns (95th)',
    'Turns (99th)',
    'Turns (max)',
    '"A" Win Rate',
    'Tie Rate',
]
FORMATS = (
    "",
    "",
    ".3f",
    ".0f",
    ".0f",
    ".0f",
    ".0f",
    ".0f",
    ".1%",
    ".1%",
)


class Outcome(Enum):
    A = 1
    Tie = 0
    B = -1


class GameResult(NamedTuple):
    outcome: Outcome
    wars: int
    rounds: int


class RoundResult(NamedTuple):
    PlayerA: str
    PlayerB: str
    FreqKhz: float
    TurnsMedian: int
    Turns90th: int
    Turns95th: int
    Turns99th: int
    TurnsMax: int
    AWinsRate: float
    TieRate: float


def CompileResults(
        player_a: str,
        player_b: str,
        games: List[GameResult],
        elapsed: timedelta,
) -> RoundResult:
    elapsed_ms = elapsed.total_seconds() * 1000
    _, bins = numpy.histogram([g.rounds for g in games], bins=100)

    return RoundResult(
        PlayerA=player_a,
        PlayerB=player_b,
        FreqKhz=len(games) / elapsed_ms,
        TurnsMedian=bins[50],
        Turns90th=bins[90],
        Turns95th=bins[95],
        Turns99th=bins[99],
        TurnsMax=bins[100],
        AWinsRate=(sum([1 for g in games if g.outcome == Outcome.A]) /
                   len(games)),
        TieRate=(sum([1 for g in games if g.outcome == Outcome.Tie]) /
                 len(games)),
    )


def print_results(deck: Deck, results: List[RoundResult]):
    print('')
    print('### ' + deck.Name)
    print('')
    print(deck.Description)
    print('')
    print(tabulate(results, HEADERS, tablefmt='pipe', floatfmt=FORMATS))
