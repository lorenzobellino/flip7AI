import numpy as np
from abc import ABC, abstractmethod

class Card(object):
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.bonus_value = ""
            self.is_bonus = False
        else:
            self.value = 0
            self.bonus_value = value
            self.is_bonus = True

    def __repr__(self):
        return str(self.value) if not self.is_bonus else self.bonus_value

class Player(ABC): # Inherit from ABC for proper abstract classes
    def __init__(self):
        self.hand = []
        self.still_in_round = True
        self.score = 0
        self.total_score = 0
        self.second_chance = False
        self.flip7 = False

    @abstractmethod
    def ask_card(self, game) -> bool:
        pass

    def busted(self) -> bool:
        value_cards = [card for card in self.hand if not card.is_bonus]
        card_set = set(card.value for card in value_cards)
        if(len(card_set) != len(value_cards)):
            if self.second_chance == False:
                return True
            else:
                # remove duplicates keeping one of each
                unique_values = set()
                new_hand = []
                for card in self.hand:
                    if not card.is_bonus:
                        if card.value not in unique_values:
                            unique_values.add(card.value)
                            new_hand.append(card)
                    else:
                        new_hand.append(card)
                self.hand = new_hand
                self.second_chance = False
        return False

        

    def count_score(self) -> int:
        if not self.hand: return 0
        
        # if no values cards, score is 0
        if all(card.is_bonus for card in self.hand):
            return 0
        
        # base points
        score = sum(card.value for card in self.hand if not card.is_bonus)
        
        # bonuses
        for card in self.hand:
            if card.is_bonus and "+" in card.bonus_value:
                score += int(card.bonus_value.replace("+", ""))
        
        # X2 bonus
        if any(card.bonus_value == "x2" for card in self.hand):
            score *= 2
        
        # Flip 7
        value_cards = [c for c in self.hand if not c.is_bonus or c.bonus_value == "0"]
        if len(value_cards) >= 7:
            score += 15

        return score

class Flip7Game(object):
    def __init__(self, players, infinite_deck=False):
        self.players = players
        self.deck = self.create_deck()
        self.infinite_deck = infinite_deck
        self.player_cores = {player: player.count_score() for player in players}

    def create_deck(self):
        deck = []
        for i in range(0, 13):
            for _ in range(i + 1):
                deck.append(Card(i))
        
        bonus_cards = ["+2", "+4", "+6", "+8", "+10", "x2", 
                       "Second Chance", "Second Chance", "Second Chance", 
                       "Flip 3", "Flip 3", "Flip 3", 
                       "Freeze", "Freeze", "Freeze"]
        for bonus in bonus_cards:
            deck.append(Card(bonus))
        
        np.random.shuffle(deck)
        return deck

    def resolve_draw(self, player, target_player=None):
        """
        Handles drawing a card and all side effects.
        target_player is used specifically for the 'Flip 3' effect.
        """
        if not self.deck:
            return

        card = self.deck.pop()
        
        # Infinite deck logic
        if self.infinite_deck:
            self.deck.append(card)
            np.random.shuffle(self.deck)

        # 1. Determine who is actually affected by this card
        # Usually the player drawing, unless it's a Flip 3 resolution
        receiver = target_player if target_player else player

        # 2. Process Card Effects
        if not card.is_bonus:
            receiver.hand.append(card)
        
        elif card.bonus_value == "Second Chance":
            receiver.second_chance = True
            
        elif card.bonus_value == "Freeze":
            # The player who DREW the card chooses who to freeze
            victim = player.choose_to_freeze(self.players)
            victim.still_in_round = False # Simply ends their round
            
        elif card.bonus_value == "Flip 3":
            # The player who DREW the card chooses who must flip 3
            victim = player.choose_to_flip3(self.players)
            for _ in range(3):
                if victim.still_in_round: # Stop if they bust mid-flip
                    self.resolve_draw(player, target_player=victim)
        
        elif "+" in card.bonus_value or card.bonus_value == "x2":
            receiver.hand.append(card)

        # 3. Check for Bust (This happens after any card is added to a hand)
        if receiver.busted():
            receiver.still_in_round = False
            receiver.hand = []

        # 4. Check for Flip 7 condition
        value_cards = [c for c in receiver.hand if not c.is_bonus]
        if len(value_cards) >= 7:
            receiver.flip7 = True

    def run(self):
        while all(p.total_score < 300 for p in self.players): # Game ends when someone hits 300
            while any(p.still_in_round for p in self.players):
                for player in self.players:
                    if player.still_in_round:
                        if player.ask_card(self):
                            self.resolve_draw(player)
                        else:
                            player.still_in_round = False
                    if (player.flip7):
                        # Immediate end of round for all players
                        for p in self.players:
                            p.still_in_round = False
                
            
            # End of Round cleanup
            for p in self.players:
                p.total_score += p.count_score()
                p.hand = []
                p.still_in_round = True
                p.second_chance = False # Reset for next round


    # def run(self):
    #     while any(p.total_score < 300 for p in self.players):
    #         while any(p.still_in_round for p in self.players):
    #             for player in self.players:
    #                 if player.still_in_round:
    #                     if player.ask_card(self):
    #                         card = self.deck.pop()

    #                         if self.infinite_deck:
    #                             self.deck.append(card)
    #                             np.random.shuffle(self.deck)

    #                         if(card.is_bonus == false):
    #                             player.hand.append(card)

    #                         elif card.bonus_value == "Freeze":
    #                             player_to_freeze = player.choose_to_freeze()
    #                         elif card.bonus_value == "Second Chance":
    #                             player.second_chance = True
    #                         elif card.bonus_value == "Flip 3":
    #                             player_to_flip3 = player.choose_to_flip3()
    #                             for _ in range(3):
    #                                 if self.deck:
    #                                     flip_card = self.deck.pop()
    #                                     # here if flip card is an other flip3 should be resolved before drawing other cards 
    #                                     # how to do it ?
    #                                     if self.infinite_deck:
    #                                         self.deck.append(flip_card)
    #                                         np.random.shuffle(self.deck)

    #                                     if flip_card.is_bonus == true:
    #                                         if flip_card.bonus_value == "Freeze":
    #                                             player_to_flip3 = player.choose_to_freeze()
    #                                         elif flip_card.bonus_value == "Second Chance":
    #                                             player_to_flip3.second_chance = True
    #                                         elif flip_card.bonus_value == "Flip 3":
    #                                             # Nested Flip 3 handling can be complex; for simplicity, we skip it here
    #                                             pass
    #                                     else:
    #                                         player_to_flip3.hand.append(flip_card)

    #                                     if player_to_flip3.busted():
    #                                         player_to_flip3.still_in_round = False
                                        
    #                         else:
    #                             player.hand.append(card)
                            
    #                         if player.busted():
    #                             player.still_in_round = False
    #                             player.hand = [] 
    #                     else:
    #                         player.still_in_round = False
    #         for p in self.players:
    #             p.score = p.count_score()
    #             p.total_score += p.score
    #             p.hand = []
    #             p.still_in_round = True

    #     return {p: p.count_score() for p in self.players}