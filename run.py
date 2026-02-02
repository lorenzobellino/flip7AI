# run a game between two probabilistic players
from flip7.objectsV2 import Flip7Game
from ProbabilisticAgent import ProbabilisticAgent
from RandomAgent import RandomAgent

if __name__ == "__main__":
    players = [
        ProbabilisticAgent(treshold=0.21, name="AI_Player_1"),
        ProbabilisticAgent(treshold=0.205, name="AI_Player_2"),
        ProbabilisticAgent(treshold=0.15, name="AI_Player_3"),
        RandomAgent(name="Random_Player"),
    ]
    # game = Flip7Game(players, infinite_deck=True)
    # game.run()
    # for player in players:
    #     print(f"{player.name} final score: \t{player.total_score}")

    # run 1000 games and collect stats
    stats = {player.name: 0 for player in players}
    num_games = 1000
    for _ in range(num_games):
        game = Flip7Game(players, infinite_deck=True)
        game.run()
        # find winner
        winner = max(players, key=lambda p: p.total_score)
        # print(f"Winner: {winner.name} with score {winner.total_score}")
        # # print all players scores
        # for player in players:
        #     print(f"{player.name} score: {player.total_score}")
        # input()
        stats[winner.name] += 1
        # reset players for next game
        for player in players:
            player.reset()
    print("\nAfter 1000 games:")
    for player_name, wins in stats.items():
        print(f"{player_name} won {wins} times ({(wins/num_games)*100:.2f}%)")

    # run 1000 games and collect average scores no infinite deck
    score_sums = {player.name: 0 for player in players}
    stats = {player.name: 0 for player in players}
    num_games = 1000
    for _ in range(num_games):
        game = Flip7Game(players, infinite_deck=False)
        game.run()
        for player in players:
            score_sums[player.name] += player.total_score
        winner = max(players, key=lambda p: p.total_score)
        stats[winner.name] += 1
        # reset players for next game
        for player in players:
            player.reset()
    print("\nAfter 1000 games (no infinite deck):")
    for player_name, wins in stats.items():
        print(f"{player_name} won {wins} times ({(wins/num_games)*100:.2f}%)")

    print("\nAverage scores after 1000 games (no infinite deck):")
    for player_name, total_score in score_sums.items():
        average_score = total_score / num_games
        print(f"{player_name} average score: {average_score:.2f}")
