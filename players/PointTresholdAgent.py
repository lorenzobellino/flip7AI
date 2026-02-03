
from flip7.objects import Player

class PointTresholdAgent(Player):
    def __init__(self, treshold, name="Dumb_Agent"):
        super().__init__() 
        self.name = name
        self.treshold = treshold

    def ask_card(self, game) -> bool:
        if self.second_chance:
            return True
        if self.count_score() < self.treshold:
            return True
        return False

    # def choose_to_freeze(self, players):
    #     """Choose the most threatening player to flip 3 cards"""
    #     potential_targets = [p for p in players if p != self and p.still_in_round]
    #     if not potential_targets:
    #         return self # No one to freeze
        
    #     # For now, just choose the player with the highest total score
    #     return max(potential_targets, key=lambda p: p.total_score)

    # def choose_to_flip3(self, players):
    #     """Choose the most threatening player to flip 3 cards"""
    #     potential_targets = [p for p in players if p != self and p.still_in_round]
    #     if not potential_targets:
    #         return self # No one to freeze
        
    #     # For now, just choose the player with the highest total score
    #     return max(potential_targets, key=lambda p: p.total_score)

