from collections import deque
from numpy.random import default_rng
from typing import Deque, List, Tuple

rng = default_rng()


class Deck(object):
    def __init__(self, name: str, description: str, cards: List[int]):
        self.Name = name
        self.Description = description
        self.cards = cards

    def deal(self) -> Tuple[Deque[int], Deque[int]]:
        playerA = deque(maxlen=len(self.cards))  # type: Deque[int]
        playerB = deque(maxlen=len(self.cards))  # type: Deque[int]
        rng.shuffle(self.cards)
        half_point = len(self.cards) // 2
        playerA.extend(self.cards[:half_point])
        playerB.extend(self.cards[half_point:])

        return playerA, playerB
