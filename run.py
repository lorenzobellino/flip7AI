

# run a game between two probabilistic players
from flip7.objects import Flip7Game
from ProbabilisticAgent import ProbabilisticAgent
from RandomAgent import RandomAgent

if __name__ == "__main__":
    players = [
        ProbabilisticAgent(treshold=0.5, name="AI_Player_1"), 
        ProbabilisticAgent(treshold=0.15,name="AI_Player_2"),
        ProbabilisticAgent(treshold=0.03,name="AI_Player_3"),
        RandomAgent(name="Random_Player")]
    
    # run 1000 games and track wins
    wins = {player.name: 0 for player in players}
    num_games = 1000
    print("-----------------------------------")
    print("Running games with infinite deck:")
    print("-----------------------------------")
    for _ in range(num_games):
        game = Flip7Game(players, infinite_deck=True)
        game.run()
        # determine winner
        scores = {player.name: player.total_score for player in players}
        winner = max(scores, key=scores.get)
        wins[winner] += 1
        # reset players for next game
        for player in players:
            player.reset()
    # print results
    for player_name, win_count in wins.items():
        print(f"{player_name} won {win_count} out of {num_games} games ({(win_count/num_games)*100:.2f}%)")

    # run 1000 games and track wins (no infinite deck)
    wins = {player.name: 0 for player in players}
    num_games = 1000
    print("-----------------------------------")
    print("Running games with finite deck:")
    print("-----------------------------------")
    for _ in range(num_games):
        game = Flip7Game(players, infinite_deck=False)
        game.run()
        # determine winner
        scores = {player.name: player.total_score for player in players}
        winner = max(scores, key=scores.get)
        wins[winner] += 1
        # reset players for next game
        for player in players:
            player.reset()
    # print results
    for player_name, win_count in wins.items():
        print(f"{player_name} won {win_count} out of {num_games} games ({(win_count/num_games)*100:.2f}%)")

    

