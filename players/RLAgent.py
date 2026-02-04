import logging
import random
import numpy as np
import operator as op
import sys
import pickle
from flip7.objects import Player

NUM_MATCHES = 5000
SAVE_POLICY = True
LOG_FREQ = 1000


class RLAgent(Player):
    """A reinforcement learning agent that learns to play Quarto."""

    def __init__(self, name="RL_Agent", verbose = False) -> None:
        super().__init__()
        self.name = name
        self.verbose = verbose
        self.is_learning = False
        self.G = dict()
        self.current_state = dict()
        self.randomness = 0.7
        self.learning_rate = 10e-3
        self.episode_history = []
        self.discount_factor = 1.0
        self.reward_weights = {
            "win": 1.0,
            "loss": -1.0,
            "hands": 0.01,
            "bust": -0.25,
            "score": 0.01,
            "game_bonus": 0.5,
        }

    def get_policy(self) -> dict:
        """Returns the policy of the agent."""
        return self.G

    def set_learning(self, is_learning: bool) -> None:
        """Sets the learning mode of the agent."""
        self.is_learning = is_learning

    def reset(self):
        """Reset agent state for a new round."""
        super().reset()
        self.episode_history = []

    def encode_state(self, game) -> dict:
        """Encode the current game state into features for learning."""
        hand_sum = sum(card.value for card in self.hand if not card.is_bonus)
        num_cards = len(self.hand)
        current_score = self.count_score()
        
        state = {
            "hand_sum": hand_sum,
            "num_cards": num_cards,
            "current_score": current_score,
            "has_second_chance": self.second_chance,
            "has_flip7": self.flip7,
        }
        return state

    def ask_card(self, game) -> bool:
        """Decide whether to ask for another card using learned policy."""
        # Encode current state
        state = self.encode_state(game)
        
        # Epsilon-greedy action selection
        if self.is_learning and random.random() < self.randomness:
            # Explore: random action
            action = random.choice([True, False])
        else:
            # Exploit: use learned policy
            state_key = str(state)
            
            # Get Q-values for both actions
            q_ask = self.G.get((state_key, True), [0])
            q_stop = self.G.get((state_key, False), [0])
            
            # Calculate average Q-values
            q_ask_val = np.mean(q_ask) if isinstance(q_ask, list) else q_ask
            q_stop_val = np.mean(q_stop) if isinstance(q_stop, list) else q_stop
            
            # Choose action with highest Q-value
            action = q_ask_val >= q_stop_val
        
        # Record state-action pair for learning
        self.episode_history.append((state, action))
        
        if self.verbose:
            print(f"{self.name} - State: {state} | Action: {'ask' if action else 'stop'}")
        
        return action

    def compute_reward(
        self,
        won: bool | None,
        hands_played: int = 0,
        busted_count: int = 0,
        total_score: int | None = None,
        game_bonus: float = 0.0,
    ) -> float:
        """Compute shaped reward using match outcome and auxiliary metrics."""
        if won is None:
            win_component = 0.0
        else:
            win_component = self.reward_weights["win"] if won else self.reward_weights["loss"]
        hands_component = self.reward_weights["hands"] * max(0, hands_played)
        bust_component = self.reward_weights["bust"] * max(0, busted_count)
        score_component = 0.0
        if total_score is not None:
            score_component = self.reward_weights["score"] * total_score

        bonus_component = self.reward_weights["game_bonus"] * game_bonus

        return win_component + hands_component + bust_component + score_component + bonus_component

    def learn(
        self,
        won: bool | None,
        hands_played: int = 0,
        busted_count: int = 0,
        total_score: int | None = None,
        game_bonus: float = 0.0,
    ) -> None:
        """Updates the policy using shaped reward and Monte Carlo learning."""
        reward = self.compute_reward(won, hands_played, busted_count, total_score, game_bonus)

        # Calculate discounted return (in reverse chronological order of states)
        G = reward
        for state, action in reversed(self.episode_history):
            state_key = str(state)
            state_action_key = (state_key, action)

            # Initialize state-action value if not seen before
            if state_action_key not in self.G:
                self.G[state_action_key] = []

            # Store the return for this state-action pair
            self.G[state_action_key].append(G)

            # Update estimated value (average of returns)
            _estimated_value = np.mean(self.G[state_action_key])

            # Optional discounting per step
            G *= self.discount_factor

        self.episode_history = []  # Reset for next episode

    
    def qlearn(self, won: bool, current_state, action, next_state, reward=None) -> None:
        """Updates Q-values using Q-learning."""
        if reward is None:
            reward = 1 if won else -1
        
        state_action_key = (str(current_state), action)
        
        # Get max Q-value for next state
        next_state_key = str(next_state)
        max_next_q = max([self.G.get((next_state_key, a), 0) for a in [True, False]])
        
        # Q-learning update
        old_q = self.G.get(state_action_key, 0)
        new_q = old_q + self.learning_rate * (reward + 0.99 * max_next_q - old_q)
        self.G[state_action_key] = new_q






