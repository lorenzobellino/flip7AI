from players import ProbabilisticAgent, RandomAgent, GAAgent, PointTresholdAgent, RLAgent
from flip7.objects import Flip7Game
import random
import os
import json
import sys
import pickle
import operator as op

NUM_MATCHES = 5000
SAVE_POLICY = True
LOG_FREQ = 100


def train():
    """Function to train RL agents."""
    from players import RLAgent, RandomAgent, ProbabilisticAgent
    
    # Create RL agent
    rl_agent = RLAgent(name="RL_Agent", verbose=False)
    rl_agent.set_learning(True)
    
    # Training phase
    print("Starting RL Training...")
    opponents = [
        RandomAgent(name="Random_Agent"),
        ProbabilisticAgent(treshold=0.19, name="Prob_AI19")
    
    ]

    # opponent = ProbabilisticAgent(treshold=0.19, name="Prob_AI19")
    opponent = RandomAgent(name="Random_Agent")
    
    best_win_rate = 0
    win_history = []
    
    totalWin = 0

    game = Flip7Game([rl_agent, opponent], infinite_deck=True)
    for episode in range(NUM_MATCHES):
        # # Randomly select an opponent
        # opponent = random.choice(opponents)
        # opponent_copy = opponent.__class__(name=opponent.name)  # Fresh opponent instance
        
        def on_round_end(round_game, _round_index):
            rounds = round_game.rounds.get(rl_agent, [])
            if not rounds:
                return

            round_info = rounds[-1]
            round_score = round_info.get("score", 0)
            busted = 1 if round_info.get("busted") else 0

            projected_totals = {
                p: p.total_score + p.count_score() for p in round_game.players
            }
            final_round = any(total >= 300 for total in projected_totals.values())
            winner = max(projected_totals, key=projected_totals.get)
            won_flag = (winner == rl_agent) if final_round else None
            game_bonus = 1.0 if won_flag is True else (-1.0 if won_flag is False else 0.0)

            rl_agent.learn(
                won_flag,
                hands_played=1,
                busted_count=busted,
                total_score=round_score,
                game_bonus=game_bonus,
            )

        # Run game
        game.run(on_round_end=on_round_end)
        
        # Determine winner and reward
        winner = max(game.players, key=lambda p: p.total_score)
        won = winner == rl_agent
        if won:
            totalWin += 1
        
        # Learning happens per round in on_round_end
        
        # Logging
        if (episode + 1) % LOG_FREQ == 0:
            print(f"Episode {episode + 1}/{NUM_MATCHES}")
            print(f"Last match: {rl_agent.name} {'won' if won else 'lost'}")
            # print(f"RL Score: {rl_agent.total_score}, {opponent_copy} Score: {opponent_copy.total_score}")
            print(f"RL Score: {rl_agent.total_score}, {opponent} Score: {opponent.total_score}")
            win_rate = totalWin / ( LOG_FREQ)
            win_history.append(win_rate)
            print(f"Win Rate: {win_rate*100:.2f}% over last {LOG_FREQ} episodes (W:{totalWin} L:{LOG_FREQ - totalWin})")
            print("------------------------------")
            totalWin = 0
            if win_rate > best_win_rate:
                best_win_rate = win_rate

           
        
        # Reset for next episode
        game.reset()
        rl_agent.reset()
    
    print(f"Best Win Rate during training: {best_win_rate*100:.2f}%")
    
    # Save policy
    if SAVE_POLICY:
        policy_file = "policies/rl_policy.pkl"
        os.makedirs("policies", exist_ok=True)
        with open(policy_file, "wb") as f:
            pickle.dump(rl_agent.get_policy(), f)
        print(f"Policy saved to {policy_file}")
    
    print("Training complete!")
    return rl_agent


if __name__ == "__main__":
    train()