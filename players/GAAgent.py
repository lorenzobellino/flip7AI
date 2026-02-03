import random
from flip7.objects import Player

class GAAgent(Player):
    def __init__(self, genome, name="GAAgent"):
        super().__init__()
        self.name = name
        self.set_genome(genome)

    def __repr__(self):
        return f"{self.name}"

    def set_genome(self, genome):
        """Set the genome for this agent. The genome is a list of parameters that will influence the agent's behavior."""
        self.genome = genome

    def cook_game_state(self,game):
        """Extract relevant features from the game state for decision making."""
        # this must return a dictionary 
        # number of value cards in hand
        value_cards = sum(1 for card in self.hand if card.is_bonus == False)
        if value_cards == 0:
            value_cards = 0.00001  # avoid division by zero

        # hand score
        hand_score = self.count_score()

        return {
            "value_cards": value_cards,
            "hand_score": hand_score,
        }




    def ask_card(self, game) -> bool:
        
        if self.second_chance:
            return True

        data = self.cook_game_state(game)


        result = data["hand_score"] * self.genome["alpha"] + self.genome["beta"] * data["value_cards"]



        # print(f"Decision : {result} | Hand Score: {data['hand_score']} (Alpha: {self.genome['alpha']}) | Value Cards: {data['value_cards']} (Beta: {self.genome['beta']})")
        # print(f"{data['hand_score']} > {self.genome['alpha']} and {data['value_cards']} < {self.genome['beta']}")
        # input()
        return result > 0


        # return score_treshold > self.genome["ask_treshold"]


    

