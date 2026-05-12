import random


class ReinforceAgent:
    """
    Placeholder REINFORCE-style agent.

    This file keeps the repository structure ready for the RL part.
    For now, it uses a simple exploratory policy over current candidates.
    Later, this can be replaced with an actual PyTorch policy network.
    """

    def __init__(self, word_list, epsilon=0.2, learning_rate=0.1):
        self.word_list = word_list
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.word_scores = {
            word: 1.0 for word in word_list
        }


    def choose_guess(self, env, state):
        candidates = state["candidates"]

        if not candidates:
            return random.choice(self.word_list)

        if random.random() < self.epsilon:
            return random.choice(self.word_list)

        # Choose based on word scores
        if random.random() < self.epsilon:
            return random.choice(candidates)

        return max(
            candidates,
            key=lambda word: self.word_scores.get(word, 1.0)
        )

    def update(self, episode_guesses, reward):
        """
        Reward or punish words used in an episode.
        """

        for guess in episode_guesses:
            old_score = self.word_scores.get(guess, 1.0)

            self.word_scores[guess] = old_score + self.learning_rate * reward

            # prevent score from going negative
            if self.word_scores[guess] < 0.01:
                self.word_scores[guess] = 0.01
        
    def train(self, env, episodes=1000):
        for episode in range(episodes):
            state = env.reset()
            done = False
            episode_guesses = []

            while not done:
                guess = self.choose_guess(env, state)
                episode_guesses.append(guess)

                state, reward, done, info = env.step(guess)

            final_reward = 1.0 if info["won"] else -1.0

            # Bonus for solving faster
            if info["won"]:
                final_reward += (6 - info["guess_number"]) * 0.2

            self.update(episode_guesses, final_reward)

        print(f"Finished training REINFORCE-style agent for {episodes} episodes.")