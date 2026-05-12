import random


class DQNAgent:
    """
    Placeholder DQN-style agent.

    This gives the repo a complete file structure without requiring PyTorch yet.
    Later, this can be expanded into a real DQN with:
        - state encoder
        - Q-network
        - replay buffer
        - target network
        - epsilon-greedy exploration
    """

    def __init__(self, word_list, epsilon=0.1):
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
        print("DQN training placeholder.")
        print(f"Would train for {episodes} episodes.")