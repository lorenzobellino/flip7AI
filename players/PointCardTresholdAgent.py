from flip7 import Player


class PointCardTresholdAgent(Player):
    def __init__(self, point_treshold, card_treshold, name="PointCardTresholdAgent"):
        super().__init__()
        self.name = name
        self.point_threshold = point_treshold
        self.card_threshold = card_treshold

    def ask_card(self, game) -> bool:
        if self.second_chance:
            return True
        if self.count_score() < self.point_threshold or len(self.hand) < self.card_threshold:
            return True
        return False