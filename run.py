

# run a game between two probabilistic players
from flip7.objectsV2 import Flip7Game
from flip7Player import ProbabilisticAgent

if __name__ == "__main__":
    players = [ProbabilisticAgent("AI_Player_1"), ProbabilisticAgent("AI_Player_2")]
    game = Flip7Game(players, infinite_deck=True)
    game.run()
    for player in players:
        print(f"{player.name} final score: {player.total_score}")

