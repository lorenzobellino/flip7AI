from flip7.objects import Player


class YesManAgent(Player):
    def __init__(self, name="YesManAgent", verbose = False):
        super().__init__()
        self.name = name
        self.verbose = verbose

    def ask_card(self, game) -> bool:
        if self.verbose:
            print(f"{self.name} chose to ask for another card.")
        return True

    def __repr__(self):
        return f"{self.name}"