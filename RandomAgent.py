import random
from flip7.objectsV2 import Player


class RandomAgent(Player):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def ask_card(self, game) -> bool:

        return random.choice([True, False])

    def choose_to_freeze(self, players):
        """Target a random player. not themselves if possible."""
        possible_targets = [p for p in players if p != self]
        if not possible_targets:
            return self
        return random.choice(possible_targets)

    def choose_to_flip3(self, players):
        """Target a random choice to flip 3 cards"""
        return random.choice(players)
