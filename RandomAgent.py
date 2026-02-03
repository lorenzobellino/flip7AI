from flip7.objects import Player
import random

class RandomAgent(Player):
    def __init__(self, name="RandomAgent"):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def ask_card(self, game) -> bool:
        # Randomly decide to ask for a card or not
        return random.choice([True, False])

    def choose_to_freeze(self, players):
        """Choose a random player to freeze. possibly not himself"""
        opponents = [p for p in players if p != self]
        return random.choice(opponents) if opponents else self

    def choose_to_flip3(self, players):
        """Choose a random player to flip 3 cards from. possibly not himself"""
        opponents = [p for p in players if p != self]
        return random.choice(opponents) if opponents else self