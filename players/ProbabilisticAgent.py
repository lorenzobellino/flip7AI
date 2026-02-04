from flip7.objects import Player

class ProbabilisticAgent(Player):
    def __init__(self, treshold = 0.03, name="Agent", verbose = False):
        super().__init__()
        self.name = name
        self.treshold = treshold  # Base treshold for bust probability
        self.verbose = verbose

    def __repr__(self):
        return f"{self.name}"

    def get_remaining_deck_composition(self, game):
        """
        In a real game, the agent knows what's in its hand, 
        but 'game.deck' represents the hidden remaining cards.
        """
        return game.deck

    def calculate_bust_probability(self, game):
        remaining_deck = self.get_remaining_deck_composition(game)
        if not remaining_deck:
            return 0
        
        # Values currently in hand that would cause a bust
        current_values = {card.value for card in self.hand if not card.is_bonus}
        
        # Count how many cards in the remaining deck have these values
        bust_cards = 0
        for card in remaining_deck:
            if not card.is_bonus and card.value in current_values:
                bust_cards += 1
        
        return bust_cards / len(remaining_deck)

    def ask_card(self, game) -> bool:
        
        # 1. If we already have 7 unique cards, the rule says we stop anyway.
        value_cards = [c for c in self.hand if not c.is_bonus]
        if len(set(c.value for c in value_cards)) >= 7:
            return False

        # 2. Calculate risk
        bust_prob = self.calculate_bust_probability(game)
        
        # 3. Aggression Logic
        # If we have a second chance, we can be much riskier (risk up to 80%)
        # If not, we stay safe (stay if risk > 25%)
        # treshold = 0.80 if self.second_chance else 0.25

        treshold = self.treshold 
        if self.second_chance:
            treshold = 1 # no risk limit with second chance


        # 4. Contextual adjustment: If an opponent is about to win the game (300 pts)
        # we might need to take bigger risks.
        leader_score = max(p.total_score for p in game.players)
        if leader_score > 250 and self.total_score < leader_score:
            treshold += 0.15 

        res = bust_prob < treshold
        if self.verbose:
            if res:
                print(f"{self.name}{'*' if self.second_chance else ''} chose to ask for another card.")
            else:
                print(f"{self.name}{'*' if self.second_chance else ''} chose to stop asking for cards.")
        return bust_prob < treshold

    # def choose_to_freeze(self, players):
    #     """Target the player with the highest current round score."""
    #     potential_targets = [p for p in players if p != self and p.still_in_round]
    #     if not potential_targets:
    #         return self # No one to freeze
        
    #     # Sort by current round score descending
    #     return max(potential_targets, key=lambda p: p.count_score())

    # def choose_to_flip3(self, players):
    #     """Target the player with the most cards (highest risk of busting)."""
    #     potential_targets = [p for p in players if p != self and p.still_in_round]
    #     if not potential_targets:
    #         return self
        
    #     # Target the person with the most unique values (highest bust prob)
    #     return max(potential_targets, key=lambda p: len([c for c in p.hand if not c.is_bonus]))