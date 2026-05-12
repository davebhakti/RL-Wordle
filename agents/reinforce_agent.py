import random


class ReinforceAgent:
    """
    Placeholder REINFORCE-style agent.

    This file keeps the repository structure ready for the RL part.
    For now, it uses a simple exploratory policy over current candidates.
    Later, this can be replaced with an actual PyTorch policy network.
    """

    def __init__(self, word_list, epsilon=0.2):
        self.word_list = word_list
        self.epsilon = epsilon

    def choose_guess(self, env, state):
        candidates = state["candidates"]

        if not candidates:
            return random.choice(self.word_list)

        if random.random() < self.epsilon:
            return random.choice(self.word_list)

        return random.choice(candidates)

    def train(self, episodes=1000):
        print("REINFORCE training placeholder.")
        print(f"Would train for {episodes} episodes.")