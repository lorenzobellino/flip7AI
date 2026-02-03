# run a game between two probabilistic players
from flip7.objects import Flip7Game
from players import (
    ProbabilisticAgent,
    RandomAgent,
    PointTresholdAgent,
    PointCardTresholdAgent,
    GAAgent,
)


def run_tournament():
    # players = [
    #     ProbabilisticAgent(treshold=0.995, name="AI_Player_1"),
    #     ProbabilisticAgent(treshold=0.95,name="AI_Player_2"),
    #     RandomAgent(name="Random_Player")]

    run_tournament()

    genome = {
        "alpha": -80.63788249552616,
        "beta": -104.51884131879049,
        "ask_treshold": 0.9387703410190069,
    }
    players = [
        # RandomAgent(name="Random_Player_1"),
        # PointTresholdAgent(treshold=20, name="Dumb_Player_20"),
        # PointTresholdAgent(treshold=30, name="Dumb_Player_30"),
        # ProbabilisticAgent(treshold=0.25,name="Prob_AI25"),
        GAAgent(genome=genome, name="My_GA_Agent"),
        ProbabilisticAgent(treshold=0.19, name="Prob_AI19"),
    ]

    # run 1000 games and track wins
    wins = {player.name: 0 for player in players}
    num_games = 1000
    print("-----------------------------------")
    print("Running games with infinite deck:")
    print("-----------------------------------")
    game = Flip7Game(players, infinite_deck=True)
    for _ in range(num_games):
        game.run()
        # determine winner
        scores = {player.name: player.total_score for player in players}
        # print(f"Game {_+1}: Scores: {scores}")
        winner = max(scores, key=scores.get)
        # print(f"Winner: {winner}\n")
        # input()
        wins[winner] += 1
        # reset players for next game
        print(game)
        input()
        game.reset()
    # print results
    for player_name, win_count in wins.items():
        print(
            f"{player_name} won {win_count} out of {num_games} games ({(win_count/num_games)*100:.2f}%)"
        )

    # run 1000 games and track wins (no infinite deck)
    wins = {player.name: 0 for player in players}
    num_games = 1000
    print("-----------------------------------")
    print("Running games with finite deck:")
    print("-----------------------------------")
    game = Flip7Game(players, infinite_deck=False)
    for _ in range(num_games):
        game.run()
        # determine winner
        scores = {player.name: player.total_score for player in players}
        winner = max(scores, key=scores.get)
        wins[winner] += 1
        # reset players for next game
        game.reset()
    # print results
    for player_name, win_count in wins.items():
        print(
            f"{player_name} won {win_count} out of {num_games} games ({(win_count/num_games)*100:.2f}%)"
        )


def run_single():
    # genome = {'alpha': 28, 'beta': 4, 'ask_treshold': 0.9387703410190069}
    genome = {
        "alpha": -3.1616193485730593,
        "beta": 69.83038018737267,
        "ask_treshold": 0.10172886631406974,
    }
    players = [
        GAAgent(genome=genome, name="My_GA_Agent"),
        ProbabilisticAgent(treshold=0.19, name="Prob_AI19"),
    ]

    game = Flip7Game(players, infinite_deck=True)
    game.run()
    print(game)


if __name__ == "__main__":

    # run_tournament()
    run_single()

    print("\nAverage scores after 1000 games (no infinite deck):")
    for player_name, total_score in score_sums.items():
        average_score = total_score / num_games
        print(f"{player_name} average score: {average_score:.2f}")
