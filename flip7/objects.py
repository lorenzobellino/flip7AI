
import numpy as np
from abc import abstractmethod
import copy


class Player(object):
    def __init__(self, game):
        self.game = game
        self.hand = []
        self.still_in_round = True
        self.score = 0

    @abstractmethod
    def ask_card(self, game) -> bool:
        pass

    @abstractmethod
    def busted(self) -> bool:
        pass

    def count_score(self) -> int:
        score = 0
        value_cards = [cards for cards in self.hand[self] if not cards.is_bonus]
        for card in value_cards:
            score += card.get_value()
        
        times2 = any(card.bonus_value == "x2" for card in self.hand[self])
        if times2:
            score *= 2
        
        # Additional bonus cards can be handled here
        bonuses = [card.bonus_value for card in self.hand[self] if card.is_bonus and card.bonus_value != "x2"]
        for bonus in bonuses:
            bonus_value = int(bonus.replace("+", ""))
            score += bonus_value

        # flip7 rule
        if len(value_cards) == 7:
            score += 15

        return score

    def get_game(self):
        return self.game


class Card(object):
    def __init__(self, value):
        if(isinstance(value, int)):
            self.value = int(value)
            self.bonus_value = ""
            self.is_bonus = False
        else:
            self.value = 0
            self.bonus_value = value
            self.is_bonus = True

    def get_value(self) -> int:
        return self.value


class Flip7Game(object):
    def __init__(self, players, infinite_deck=False):
        self.players = players
        self.hands = {player: [] for player in players}
        self.deck = self.create_deck()
        np.random.shuffle(self.deck)
        self.infinite_deck = infinite_deck
            

    def create_deck(self):
        deck = []
        # one 0, one 1, two 2, three 3, ..., nine 9,... twelve 12
        for i in range(0, 13):
            for _ in range(i + 1):
                deck.append(Card(i))
        # Adding bonus cards
        bonus_cards = ["+2", "+4", "+6", "+8", "+10","x2", "Second Chance", "Second Chance", "Second Chance", "Flip 3", "Flip 3", "Flip 3", "Freeze", "Freeze", "Freeze"]
        for bonus in bonus_cards:
            deck.append(Card(bonus))
        return np.random.shuffle(deck)

    def get_hands(self):
        return self.hands

    def run(self):
        while any(player.still_in_round for player in self.players):
            for player in self.players:
                if player.still_in_round:
                    if player.ask_card(self):
                        card = self.deck.pop()
                        if(self.infinite_deck):
                            self.deck.append(card)
                            np.random.shuffle(self.deck)
                        player.hand.append(card)
                        if(player.busted()):
                            player.still_in_round = False
                            player.hand = []
                            player.score = 0
                    else:
                        player.still_in_round = False

        scores = {player: player.count_score() for player in self.players} 
        return scores 