import random

class RandomAgent:

    def choose_guess(self, env, state):
        return random.choice(env.word_list)